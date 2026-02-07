import pandas as pd

def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Method for transform diferent dataframes with same features
    
    :param df: dataframe to normalize
    """

    df = df.copy()

    # normalizar columna close
    if "close" in df.columns:
        df["Close"] = df["close"]
        df.drop(columns=["close"], inplace=True)

    # normalizar index a datetime sin hora
    df.index = pd.to_datetime(df.index).normalize()

    return df