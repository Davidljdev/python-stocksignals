from data.fetch_prices import fetch_price_history
from analysis.signals import detect_signals, detect_signals2
from utils.dates import calculate_price_changes
from utils.dataframe import normalize_dataframe

def analyze_asset(asset: dict) -> dict:
    """
    Analys a asset and set a set of values for validate
    """
    # name asset ticket. ex: AAPL
    ticker = asset["ticker"]
    # stock/crypto/etf
    asset_type = asset["type"]

    dataFrame = fetch_price_history(ticker)
    dataFrame = normalize_dataframe(dataFrame)

    #prices = None
    #changes = None
    #signals = { "demo": [1,2,3,4,5]}
    prices, changes = calculate_price_changes(dataFrame)
    #signals = detect_signals(changes)
    signals = detect_signals2(prices,changes)
    #print(f"=== ",ticker, " ===")
    #print(dataFrame)
    #print("=== === ===")

    return {
        "asset": ticker,
        "type": asset_type,
        "prices": prices,
        "price_changes_percent": changes,
        "signals": signals,
        "recommendation": "REVIEW" if signals else "NONE"
    }
