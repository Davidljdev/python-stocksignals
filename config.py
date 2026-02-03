# Lista de activos a analizar
ASSETS = [
    {"ticker": "SPY", "type": "etf"},
    {"ticker": "AAPL", "type": "stock"},
    {"ticker": "GOOGL", "type": "stock"},
    {"ticker": "BTC-USD", "type": "crypto"},
]

# Ventanas temporales (en días)
WINDOWS = {
    "3m": 90,
    "6m": 180,
    "12m": 365,
}

# Umbrales de alerta (porcentaje)
THRESHOLDS = {
    "drop_long": -25,
    "drop_mid": -15,
    "drop_short": -10,
    "surge_long": 40,
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
