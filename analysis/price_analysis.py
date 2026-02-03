from data.fetch_prices import fetch_price_history
from analysis.signals import detect_signals
from utils.dates import calculate_price_changes

def analyze_asset(asset: dict) -> dict:
    """
    Analiza un activo completo y devuelve el resultado estructurado.
    """
    ticker = asset["ticker"]
    asset_type = asset["type"]

    df = fetch_price_history(ticker)
    prices, changes = calculate_price_changes(df)
    signals = detect_signals(changes)

    return {
        "asset": ticker,
        "type": asset_type,
        "prices": prices,
        "price_changes_pct": changes,
        "signals": signals,
        "recommendation": "REVIEW" if signals else "NONE"
    }
