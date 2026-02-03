
from datetime import datetime, timedelta
from config import WINDOWS
import pandas as pd

def get_price_near_date(df: pd.DataFrame, target_date: datetime) -> float:
    """
    Devuelve el precio de cierre más cercano a una fecha objetivo.
    """
    df = df.copy()
    df["date_diff"] = abs(df.index - target_date)
    closest_row = df.sort_values("date_diff").iloc[0]
    return float(closest_row["Close"])

def calculate_price_changes(df: pd.DataFrame) -> dict:
    """
    Calcula cambios porcentuales para 3m, 6m y 12m.
    """
    now = datetime.today()
    current_price = float(df.iloc[-1]["Close"])

    prices = {
        "current": current_price
    }
    changes = {}

    for label, days in WINDOWS.items():
        target_date = now - timedelta(days=days)
        past_price = get_price_near_date(df, target_date)

        prices[label] = past_price
        changes[label] = round(
            (current_price - past_price) / past_price * 100, 2
        )

    return prices, changes
