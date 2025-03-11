import pandas as pd

def load_data(filepath):
    """Charge les données depuis un fichier CSV."""
    return pd.read_csv(filepath)

def preprocess_data(df, is_train=False):
    """Nettoie et transforme les données.
    - is_train=True : conserve `trip_duration` pour l'entraînement
    - is_train=False : supprime `trip_duration` pour l'inférence
    """

    # Supprimer la colonne 'id'
    df = df.drop(columns=["id"], errors="ignore")

    # Convertir 'pickup_datetime' si elle est présente
    if "pickup_datetime" in df.columns:
        df["pickup_hour"] = pd.to_datetime(df["pickup_datetime"]).dt.hour
        df = df.drop(columns=["pickup_datetime"], errors="ignore")

    # Convertir 'dropoff_datetime' si elle est présente
    if "dropoff_datetime" in df.columns:
        df["dropoff_hour"] = pd.to_datetime(df["dropoff_datetime"]).dt.hour
        df = df.drop(columns=["dropoff_datetime"], errors="ignore")
    else:
        df["dropoff_hour"] = 0  # Ajout d'une colonne factice

    # Convertir 'store_and_fwd_flag' en numérique
    if "store_and_fwd_flag" in df.columns:
        df["store_and_fwd_flag"] = df["store_and_fwd_flag"].map({"N": 0, "Y": 1})

    # ⚠️ Supprimer 'trip_duration' uniquement pour l'inférence
    if not is_train:
        df = df.drop(columns=["trip_duration"], errors="ignore")

    return df
