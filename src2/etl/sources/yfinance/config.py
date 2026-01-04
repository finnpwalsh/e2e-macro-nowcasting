"""
V1 market shock sensors (Yahoo Finance)

Design goals:
- small interpretable set
- daily freq
- macro-relevant signals
"""
YF_TICKERS = [
    "SPY",  # equities risk
    "^VIX", # volatility
    "IEF",  # rates expectations
    "CL=F", # energy prices
    "UUP",  # USD strength
]

YF_RAW_SCHEMA_COLS = [
    "date",
    "value",
    "ticker",
]