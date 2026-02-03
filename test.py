import pandas as pd
import requests
from pandas_datareader import data as pdr
from datetime import datetime
import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

load_dotenv()
FMP_API_KEY = os.getenv("FMP_API_KEY")
print("FMP_API_KEY loaded:" , bool(FMP_API_KEY))
EMAIL_USER = os.getenv("EMAIL_USER")
print("EMAIL_USER KEY LOADED: ", bool(EMAIL_USER))
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_DESTINY = os.getenv("EMAIL_DESTINY")
print("EMAIL API KEYS LOADED: ", bool(EMAIL_USER) and bool(EMAIL_PASSWORD))

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

def test_fmp_key_metrics_stable():
    #print("\n=== TEST FMP KEY METRICS ===")
    try: 
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
    except Exception as e:
        print("TEST FMP KEY METRICS FALLÓ ❌", e)

def test_fmp_ratios_stable():
    #print("\n=== TEST FMP RATIOS ===")
    try: 
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
    except Exception as e:
            print("BINANCE FALLÓ ❌", e)

def ordenar_por_anio(data, columnas, titulo):

    if not data or not isinstance(data, list):
        print(f"X {titulo} – No data to process")
        return

    df = pd.DataFrame(data)

    df["year"] = df["date"].str[:4].astype(int)
    df = df[["year"] + columnas]
    df = df.sort_values("year").reset_index(drop=True)

    print(f"\n{titulo}")
    print(df)

def test_email():
    print("\n=== TEST EMAIL (GMAIL SMTP) ===")    

    if not EMAIL_PASSWORD or not EMAIL_DESTINY:
        print("X EMAIL FALLÓ ❌ – Variables de entorno no cargadas")
        return

    try:
        msg = EmailMessage()
        msg["Subject"] = "Test desde GitHub Actions"
        msg["From"] = EMAIL_USER
        msg["To"] = EMAIL_DESTINY
        msg.set_content("Correo enviado correctamente desde el pipeline 🚀")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print("V EMAIL OK ✅")

    except Exception as e:
        print("X EMAIL FALLÓ ❌", e)

if __name__ == "__main__":
    test_stooq()
    test_coingecko()

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

    test_email()