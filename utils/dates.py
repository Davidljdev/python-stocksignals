
from datetime import datetime, timedelta
from config import WINDOWS
import pandas as pd

def get_price_near_date(df: pd.DataFrame, target_date: datetime) -> float:
    """
    Devuelve el precio de cierre más cercano a una fecha objetivo.
    """
    # se copia el dataframe por que es mutable, es decir, 
    # si se modifica aqui, se modifica el objeto que lo puso como parametro.
    df = df.copy()

    # se usa ABS para obtener el valor absoluto, 
    # por que importa mas saber la diferencia, que saber si fue positivo o no.
    df["date_diff"] = abs(df.index - target_date)

    # se ordena el df para tener la diferencia de dias en orden
    # y luego se obtiene le primer elemento, el que esta mas cerca: date_diff 0, 1 o 2
    closest_row = df.sort_values("date_diff").iloc[0]
    return round(float(closest_row["Close"]), 2)

def calculate_price_changes(df: pd.DataFrame) -> tuple:
    # 1. Aseguramos que el DataFrame esté ordenado por fecha
    #    de fecha más antigua → más reciente
    df = df.sort_index()

    # 2. Tomamos la última fila (precio más reciente disponible)
    last_row = df.iloc[-1]

    # 3. Extraemos el precio de cierre actual
    current_price = float(last_row["Close"])

    # 4. Guardamos precios de referencia
    prices = {
        "Now": current_price
    }

    # 5. Diccionario para los cambios porcentuales
    changes = {}

    # 6. Recorremos las ventanas de tiempo (3m, 6m, 12m, etc.)
    for label, days in WINDOWS.items():

        # 7. En vez de usar "hoy", usamos la última fecha REAL del DataFrame
        #    Esto evita errores de timezone y días sin mercado
        #    por ej: 
        target_date = df.index[-1] - timedelta(days=days)

        # 8. Buscamos el precio más cercano a esa fecha
        past_price = get_price_near_date(df, target_date)

        # 9. Si no hay precio válido, evitamos romper el cálculo
        if past_price is None or past_price == 0:
            prices[label] = None
            changes[label] = None
            continue

        # 10. Guardamos el precio histórico
        prices[label] = past_price

        # 11. Calculamos el cambio porcentual
        # exa: si el precio actual es mayor => (120 - 100) / 100 * 100 = 20 %
        # es decir, el precio actual es 20 % mayor que el precio pasado.
        changes[label] = round(
            (current_price - past_price) / past_price * 100, 2
        )

    # 12. Devolvemos ambos diccionarios
    return prices, changes

