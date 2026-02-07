from datetime import datetime, timedelta
import pandas as pd
from pandas_datareader import data as pdr
import requests

def fetch_price_history(ticker: str, period_days: int = 365) -> pd.DataFrame:
    """
    Descarga precios históricos diarios de forma estable.
    Usa period en lugar de start/end para evitar bugs de timezone.
    """
    dataFrame = None
    if ticker == 'BTC': 
        dataFrame = get_bitcoin(period_days)
    else:
        dataFrame = get_stock_etf(ticker)    

    if dataFrame.empty or dataFrame is None:
        raise ValueError(f"No se pudieron obtener datos para {ticker}")

    return dataFrame

def get_bitcoin(days: int) -> pd.DataFrame:
    try:
        url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
        params = {"vs_currency": "usd", "days": days}
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()

        df = pd.DataFrame(data["prices"], columns=["timestamp", "close"])
        df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
        df = df.set_index("date")
        df = df.drop(columns=["timestamp"])

        return df

    except Exception as e:
        #raise ValueError("No se pudieron obtener datos para BTC") from e
        print("No se pudieron obtener datos para BTC. ", e)
        return None

def get_stock_etf(ticker: str) -> pd.DataFrame:
    try:
        if not ticker.endswith(".US"):
            ticker = ticker + ".US"

        df = pdr.DataReader(ticker, "stooq")
        return df.sort_index()

    except Exception as e:
        #raise ValueError(f"Get {ticker} failed") from e
        print(f"Get {ticker} failed. " , e)
        return None