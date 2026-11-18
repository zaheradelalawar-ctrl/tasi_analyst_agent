"""
Main Entrypoint: TASI 19-Institution Consensus & Ranking Agent.
"""

import sys
import argparse
from datetime import datetime
from fetcher import TasiAnalystFetcher
from analyzer import ConsensusRanker
from excel_exporter import ExecutiveExcelBuilder


def run_agent(demo_mode: bool = False, output_file: str = None):
    print("=" * 65)
    print("  TASI 19-INSTITUTION CONSENSUS & RANKING AGENT")
    print("=" * 65)

    print("[1/3] Ingesting analyst recommendations and 12-month target prices across all 19 institutions...")
    fetcher = TasiAnalystFetcher()
    records = fetcher.fetch_all()

    print(f"[2/3] Aggregating {len(records)} analyst recommendations & computing consensus scores...")
    ranker = ConsensusRanker(records)
    datasets = ranker.build_ranked_consensus()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    out_path = output_file or f"TASI_19_Institutions_Ranked_{timestamp}.xlsx"
    print(f"[3/3] Generating executive Excel report -> {out_path}")
    
    builder = ExecutiveExcelBuilder(output_file=out_path)
    saved_path = builder.build(datasets)

    print("\nDone! Top 5 Ranked TASI Stocks by Institutional Consensus:")
    top5 = datasets["ranked"][["rank", "symbol", "company", "consensus_signal", "composite_score", "consensus_upside_pct"]].head(5)
    print(top5.to_string(index=False))
    return saved_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TASI 19-Institution Stock Consensus & Ranking Agent")
    parser.add_argument("--demo", action="store_true", help="Run with sample dataset")
    parser.add_argument("--out", type=str, default=None, help="Custom output .xlsx file path")
    args = parser.parse_args()
    run_agent(demo_mode=args.demo, output_file=args.out)