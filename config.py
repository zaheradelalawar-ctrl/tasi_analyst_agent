"""
Configuration for the TASI 19-Institution Consensus & Ranking Agent.
"""

INSTITUTIONS = [
    {"id": "morgan-stanley-international", "name": "Morgan Stanley Saudi Arabia", "tier": "Global"},
    {"id": "united-securities", "name": "United Securities Company", "tier": "Regional"},
    {"id": "alphamena", "name": "AlphaMena", "tier": "Regional"},
    {"id": "arqaam-capital", "name": "Arqaam Capital", "tier": "Regional"},
    {"id": "ci-capital", "name": "CI Capital", "tier": "Regional"},
    {"id": "hsbc-saudi-arabia", "name": "HSBC", "tier": "Global"},
    {"id": "aljazira-capital", "name": "AlJazira Capital", "tier": "Local"},
    {"id": "bsf-capital", "name": "BSF Capital", "tier": "Local"},
    {"id": "ubhar-capital", "name": "U-Capital", "tier": "Regional"},
    {"id": "gib-capital", "name": "GIB Capital", "tier": "Local"},
    {"id": "al-rajhi-capital", "name": "Al Rajhi Capital", "tier": "Local"},
    {"id": "riyad-capital", "name": "Riyad Capital", "tier": "Local"},
    {"id": "jefferies", "name": "Jefferies", "tier": "Global"},
    {"id": "goldman-sachs", "name": "Goldman Sachs", "tier": "Global"},
    {"id": "efg-hermes", "name": "EFG Hermes", "tier": "Regional"},
    {"id": "snb-capital", "name": "SNB Capital", "tier": "Local"},
    {"id": "anb-capital", "name": "ANB Capital", "tier": "Local"},
    {"id": "jp-morgan", "name": "J.P. Morgan", "tier": "Global"},
    {"id": "alawwal-capital", "name": "Alawwal Capital", "tier": "Local"},
]

RATING_SCORES = {
    "strong buy": 5.0,
    "buy": 4.5,
    "overweight": 4.5,
    "accumulate": 4.0,
    "outperform": 4.25,
    "hold": 3.0,
    "neutral": 3.0,
    "equal-weight": 3.0,
    "equalweight": 3.0,
    "market perform": 3.0,
    "reduce": 2.0,
    "underperform": 1.75,
    "underweight": 1.5,
    "sell": 1.0,
}

# Composite Ranking Weights (Must sum to 1.0)
WEIGHTS = {
    "upside_pct": 0.45,       # Consensus upside to 12M Target Price
    "rating_score": 0.35,     # Weighted Buy/Overweight score (1 to 5)
    "coverage_depth": 0.20,   # Number of institutions covering the stock
}

ARGAAM_BASE_URL = "https://www.argaam.com/en/tadawul/tasi/{slug}/researchers-opinions"
ARGAAM_API_BASE = "https://api.argaam.com/api/v1.1"
