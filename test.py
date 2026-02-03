import pandas as pd
import requests
from pandas_datareader import data as pdr
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
FMP_API_KEY = os.getenv("FMP_API_KEY")

def test_stooq():
    print("\n=== TEST STOOQ (ACCIONES / ETF) ===")
    try:
        df = pdr.DataReader("SPY.US", "stooq")
        print(df.head())
        print("V STOOQ OK")
        print(df.index.min(), df.index.max())
        print(len(df), "filas")
    except Exception as e:
        print("X STOOQ FALLÓ", e)


def test_coingecko():
    print("\n=== TEST COINGECKO (CRIPTO) ===")
    try:
        url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
        params = {"vs_currency": "usd", "days": 365}
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        #print("Últimos precios:", data["prices"][-3:])
        print("Últimos precios:")
        for ts, price in data["prices"][-3:]:
            print(datetime.utcfromtimestamp(ts / 1000), price)
        print("V COINGECKO OK")
        print(len(data["prices"]))
    except Exception as e:
        print("X COINGECKO FALLÓ", e)


def test_binance():
    print("\n=== TEST BINANCE (CRIPTO) ===")
    try:
        url = "https://api.binance.com/api/v3/klines"
        params = {
            "symbol": "BTCUSDT",
            "interval": "1d",
            "limit": 10
        }
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        for k in data[:3]:
            print({
                "open_time": k[0],
                "open": k[1],
                "high": k[2],
                "low": k[3],
                "close": k[4],
                "volume": k[5],
            })
        print("BINANCE OK ✅")
        print(len(data))
    except Exception as e:
        print("BINANCE FALLÓ ❌", e)

def test_fmp_key_metrics_stable():
    #print("\n=== TEST FMP KEY METRICS ===")
    url = "https://financialmodelingprep.com/stable/key-metrics"
    params = {
        "symbol": "AAPL",
        "period": "annual",
        "apikey": FMP_API_KEY
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    #print(type(r.json()))
    #print(r.json()[:1])
    return r.json()

def test_fmp_ratios_stable():
    #print("\n=== TEST FMP RATIOS ===")
    url = "https://financialmodelingprep.com/stable/ratios"
    params = {
        "symbol": "AAPL",
        "period": "annual",
        "apikey": FMP_API_KEY
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    #print(type(r.json()))
    #print(r.json()[:1])
    return r.json()

def ordenar_por_anio(data, columnas, titulo):
    df = pd.DataFrame(data)

    df["year"] = df["date"].str[:4].astype(int)
    df = df[["year"] + columnas]
    df = df.sort_values("year").reset_index(drop=True)

    print(f"\n{titulo}")
    print(df)

if __name__ == "__main__":
    test_stooq()
    test_coingecko()
    test_binance()

    key_metrics = test_fmp_key_metrics_stable()
    ratios = test_fmp_ratios_stable()
    ordenar_por_anio(
        key_metrics,
        columnas=[
            "returnOnAssets",
            "returnOnCapitalEmployed",
            "returnOnEquity",
            "freeCashFlowYield",
            "evToEBITDA"
        ],
        titulo="=== KEY METRICS POR AÑO ==="
    )
    ordenar_por_anio(
        ratios,
        columnas=[
            "priceToEarningsRatio",
            "debtToEquityRatio",
            "priceToBookRatio",
            "dividendYield"
        ],
        titulo="=== RATIOS POR AÑO ==="
    )