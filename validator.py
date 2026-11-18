"""
Data Validator Module: Enforces strict schema, range, and sanity checks on institutional equity data.
Prevents unvalidated, corrupted, or hallucinated prices from reaching the final investment report.
"""

import os
import re
import logging
import pandas as pd
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class DataValidator:
    @staticmethod
    def validate_raw_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        valid_records = []
        if not records:
            logging.warning("Validator received empty records list.")
            return valid_records

        for idx, rec in enumerate(records):
            symbol = str(rec.get("symbol", "")).strip()
            company = str(rec.get("company", "")).strip()
            institution = str(rec.get("institution", "")).strip()
            
            # Sanity check symbol (must be 4 digits for TASI)
            if not re.match(r"^\d{4}$", symbol):
                logging.warning(f"Row {idx}: Invalid TASI symbol '{symbol}' for company '{company}'. Dropping record.")
                continue

            try:
                curr_price = float(rec.get("current_price", 0.0))
                target_price = float(rec.get("target_price", 0.0))
            except (ValueError, TypeError):
                logging.warning(f"Row {idx}: Non-numeric price detected for symbol {symbol}. Dropping record.")
                continue

            if curr_price <= 0.5 or curr_price > 5000.0:
                logging.warning(f"Row {idx}: Out-of-bounds current price ({curr_price}) for symbol {symbol}. Dropping record.")
                continue

            if target_price > 0 and (target_price < 0.5 or target_price > 10000.0):
                logging.warning(f"Row {idx}: Out-of-bounds target price ({target_price}) for symbol {symbol}. Resetting target to 0.")
                target_price = 0.0

            rec["current_price"] = curr_price
            rec["target_price"] = target_price
            valid_records.append(rec)

        logging.info(f"DataValidator passed {len(valid_records)} of {len(records)} raw institutional records.")
        return valid_records

    @staticmethod
    def validate_aggregated_consensus(ranked_df: pd.DataFrame) -> pd.DataFrame:
        if ranked_df.empty:
            return ranked_df

        ranked_df["composite_score"] = pd.to_numeric(ranked_df["composite_score"], errors="coerce").fillna(0.0)
        ranked_df["consensus_upside_pct"] = pd.to_numeric(ranked_df["consensus_upside_pct"], errors="coerce").fillna(0.0)
        
        if "target_dispersion_pct" in ranked_df.columns:
            ranked_df["target_dispersion_pct"] = pd.to_numeric(ranked_df["target_dispersion_pct"], errors="coerce").fillna(0.0)

        return ranked_df