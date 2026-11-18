"""
Consensus Analyzer: Processes institutional consensus data, validates records, 
calculates composite scores, and ranks TASI stocks by institutional agreement.
"""

import pandas as pd
import numpy as np
import logging
from typing import List, Dict, Any
from validator import DataValidator

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class ConsensusRanker:
    def __init__(self, records: List[Dict[str, Any]]):
        self.records = DataValidator.validate_raw_records(records)

    def build_ranked_consensus(self) -> Dict[str, pd.DataFrame]:
        if not self.records:
            logging.error("No valid records available for consensus aggregation.")
            return {"ranked": pd.DataFrame(), "matrix": pd.DataFrame()}

        df = pd.DataFrame(self.records)

        df["upside_pct"] = np.where(
            df["current_price"] > 0,
            (df["target_price"] - df["current_price"]) / df["current_price"],
            0.0
        )

        grouped = df.groupby(["symbol", "company"]).agg(
            total_calls=("institution", "count"),
            current_price=("current_price", "max"),
            median_target=("target_price", lambda x: float(x[x > 0].median()) if not x[x > 0].empty else 0.0),
            consensus_upside_pct=("upside_pct", lambda x: float(x[x != 0].median()) if not x[x != 0].empty else 0.0),
            target_dispersion_pct=("upside_pct", lambda x: float(x[x != 0].std() * 100) if len(x[x != 0]) > 1 else 0.0)
        ).reset_index()

        pos_ratings = ["strong buy", "buy", "overweight", "accumulate"]
        neg_ratings = ["sell", "underweight"]

        sentiment_stats = []
        for _, row in grouped.iterrows():
            sub = df[(df["symbol"] == row["symbol"]) & (df["company"] == row["company"])]
            ratings = sub["rating"].str.lower().str.strip().fillna("")
            
            pos = sum(any(p in r for p in pos_ratings) for r in ratings)
            neg = sum(any(n in r for n in neg_ratings) for r in ratings)
            neu = sum(not any(p in r for p in pos_ratings) and not any(n in r for n in neg_ratings) for r in ratings)
            total_f = len(sub)

            if total_f >= 4 and pos >= 3:
                status, signal = "Strong consensus (4+ firms)", "STRONG BUY"
            elif total_f >= 2 and pos >= 2:
                status, signal = "Confirmed (2+ firms)", "ACCUMULATE / BUY"
            elif pos > 0 and neg > 0:
                status, signal = "Conflicting opinions", "HOLD / MIXED"
            elif total_f == 1 and pos == 1:
                status, signal = "Single opinion", "BUY"
            elif total_f == 1 and neg == 1:
                status, signal = "Single opinion", "SELL"
            else:
                status, signal = "No confirmation", "NEUTRAL"

            sentiment_stats.append({
                "symbol": row["symbol"],
                "positive_firms": pos,
                "neutral_firms": neu,
                "negative_firms": neg,
                "status": status,
                "consensus_signal": signal
            })

        sent_df = pd.DataFrame(sentiment_stats)
        ranked = pd.merge(grouped, sent_df, on="symbol")

        ranked["composite_score"] = (
            (ranked["consensus_upside_pct"].clip(lower=0) * 100 * 0.4) +
            (ranked["positive_firms"] * 12.0) -
            (ranked["target_dispersion_pct"].fillna(0).clip(upper=100) * 0.1)
        ).round(2)

        ranked = DataValidator.validate_aggregated_consensus(ranked)

        ranked = ranked.sort_values(by="composite_score", ascending=False).reset_index(drop=True)
        ranked.insert(0, "rank", ranked.index + 1)

        return {
            "ranked": ranked,
            "matrix": df
        }