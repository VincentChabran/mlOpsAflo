import pandas as pd
import numpy as np

# Dictionnaire pour convertir les jours de la semaine
DICT_WEEKDAY = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 
                4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

def transform_target(y):
    """Transforme `trip_duration` en log(1 + y)."""
    return np.log1p(y).rename('log_trip_duration')

def preprocess_data(df, is_train=False):
    """
    Nettoie et transforme les données.

    - is_train=True : conserve `trip_duration` et applique `log_trip_duration`
    - is_train=False : supprime `trip_duration`
    """

    # Supprimer la colonne 'id'
    df = df.drop(columns=["id"], errors="ignore")

    # Convertir 'pickup_datetime' si elle est présente
    if "pickup_datetime" in df.columns:
        df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"])
        df["pickup_hour"] = df["pickup_datetime"].dt.hour
        df["weekday"] = df["pickup_datetime"].dt.weekday  # Ajout de la feature jour de la semaine
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

    # ⚠️ Appliquer la transformation log uniquement pour l'entraînement
    if is_train and "trip_duration" in df.columns:
        df["log_trip_duration"] = transform_target(df["trip_duration"])

    # ⚠️ Supprimer 'trip_duration' uniquement pour l'inférence
    if not is_train:
        df = df.drop(columns=["trip_duration"], errors="ignore")

    return df
