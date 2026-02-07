# Lista de activos a analizar
ASSETS = [
    {"ticker": "SPY", "type": "etf"},
    {"ticker": "AAPL", "type": "stock"},
    {"ticker": "GOOGL", "type": "stock"},
    {"ticker": "BRK-B", "type": "stock"},
    {"ticker": "BLK", "type": "stock"},
    {"ticker": "V", "type": "stock"},
    {"ticker": "NU", "type": "stock"},
    {"ticker": "MSFT", "type": "stock"},
    {"ticker": "AMZN", "type": "stock"},
    {"ticker": "MELI", "type": "stock"},
    {"ticker": "META", "type": "stock"},
    {"ticker": "CMG", "type": "stock"},
    {"ticker": "DPZ", "type": "stock"},
    {"ticker": "PYPL", "type": "stock"},
    {"ticker": "TSM", "type": "stock"},
    {"ticker": "ASML", "type": "stock"},
    {"ticker": "KO", "type": "stock"},
    {"ticker": "PG", "type": "stock"},
    {"ticker": "GE", "type": "stock"},
    {"ticker": "NVDA", "type": "stock"},
    {"ticker": "BTC", "type": "crypto"},
]

# Ventanas temporales (en días)
# 3m  = corto plazo (momentum)
# 6m  = medio plazo
# 12m = tendencia anual
# 24m = ciclo
# 36m = estructura / largo plazo
WINDOWS = {
    "3m": 90,
    "6m": 180,
    "12m": 365,
    "24m": 730,
    "36m": 1095
}

# Umbrales de alerta (porcentaje)
THRESHOLDS = {
    # Caídas
    "drop_short": -10,    # 3m
    "drop_mid": -20,      # 6m
    "drop_long": -30,     # 12m
    "drop_cycle": -40,    # 24m
    "drop_struct": -50,   # 36m

    # Subidas
    "surge_short": 15,    # 3m
    "surge_mid": 30,      # 6m
    "surge_long": 50,     # 12m
    "surge_cycle": 70,    # 24m
    "surge_struct": 100,  # 36m
}

# Symbols allowed by Financial Modeling Prep FREE plan (verified)
FMP_FREE_SYMBOLS = [
    "AAPL", "TSLA", "AMZN", "MSFT", "NVDA", "GOOGL", "META", "NFLX",
    "JPM", "V", "BAC", "PYPL", "DIS", "T", "PFE", "COST", "INTC",
    "KO", "TGT", "NKE", "SPY", "BA", "BABA", "XOM", "WMT", "GE",
    "CSCO", "VZ", "JNJ", "CVX", "PLTR", "SQ", "SHOP", "SBUX",
    "SOFI", "HOOD", "RBLX", "SNAP", "AMD", "UBER", "FDX", "ABBV",
    "ETSY", "MRNA", "LMT", "GM", "F", "LCID", "CCL", "DAL", "UAL",
    "AAL", "TSM", "SONY", "ET", "MRO", "COIN", "RIVN", "RIOT",
    "CPRX", "VWO", "SPYG", "NOK", "ROKU", "VIAC", "ATVI", "BIDU",
    "DOCU", "ZM", "PINS", "TLRY", "WBA", "MGM", "NIO", "C", "GS",
    "WFC", "ADBE", "PEP", "UNH", "CARR", "HCA", "TWTR", "BILI",
    "SIRI", "FUBO", "RKT"
]
