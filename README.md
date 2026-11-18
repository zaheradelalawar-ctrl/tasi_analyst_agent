# TASI 19-Institution Consensus & Ranking Agent

Modular Python agent that fetches analyst ratings and 12-month target prices across all **19 Saudi, GCC, and Global research institutions**, normalizes their rating scales, computes a weighted **Composite Alpha Score**, and exports an executive-ready, multi-tab Excel workbook (`.xlsx`).

## Project Structure
- `config.py` — Registry of all 19 institutions (Local, Regional, Global tiers), rating normalization weights (`1.0` to `5.0`), and ranking formula weights.
- `fetcher.py` — Multi-source ingestion engine supporting:
  1. **Local CSV/Excel Drop-in (`raw_exports/`)** — Automatically parses any analyst export files you place in `raw_exports/`.
  2. **Argaam Fundamentals API (`ARGAAM_API_KEY`)** — Direct JSON ingestion from `/api/v1.1/markets/3/opinions`.
  3. **Automated Web Scraper** — Fetches public researcher opinion tables for each of the 19 institutions.
- `analyzer.py` — Deduplicates calls per institution/stock, calculates Consensus Target Price, Implied Upside %, Buy/Hold/Sell counts, and Composite Rank.
- `excel_exporter.py` — Builds a 4-tab formatted workbook (`1_Ranked_Consensus`, `2_Institution_TP_Matrix`, `3_Institution_Activity`, `4_Raw_Predictions_Log`) with live Excel formulas, conditional formatting, color-coded signal badges, and a Top 10 Upside chart.
- `main.py` — CLI orchestrator (`python main.py` or `python main.py --demo`).

## Quick Start
```bash
pip install -r requirements.txt
python main.py --demo   # Generates sample ranked workbook immediately
python main.py          # Fetches live data across all 19 institutions
```
