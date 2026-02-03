from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd

def fetch_price_history(ticker: str, period: str = "15mo") -> pd.DataFrame:
    """
    Descarga precios históricos diarios de forma estable.
    Usa period en lugar de start/end para evitar bugs de timezone.
    """
    ticker_obj = yf.Ticker(ticker)
    df = ticker_obj.history(
        period=period,
        interval="1d",
        auto_adjust=True
    )

    if df.empty:
        raise ValueError(f"No se pudieron obtener datos para {ticker}")

    return df