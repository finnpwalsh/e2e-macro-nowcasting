"""
FRED anchors series configuration.

Maps internal feature names to FRED series IDs.
"""
SERIES: dict[str, str] = {
    # target
    "cpi_all_items": "CPIAUCSL",

    # features
    "cpi_energy": "CPIENGSL",
    "cpi_housing": "CPIHOSSL",
    "federal_funds": "FEDFUNDS",
    "unemployment_rate": "UNRATE",
}

