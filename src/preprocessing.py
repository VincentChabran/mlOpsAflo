import pandas as pd

def load_data(filepath):
    """Charge les données depuis un fichier CSV."""
    return pd.read_csv(filepath)

def preprocess_data(df):
    """Nettoie et transforme les données pour l'entraînement du modèle."""
    
    # Supprimer 'id' car il ne sert pas au modèle
    df = df.drop(columns=["id"], errors="ignore")
    
    # Convertir 'pickup_datetime' et 'dropoff_datetime' en datetime
    df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"])
    df["dropoff_datetime"] = pd.to_datetime(df["dropoff_datetime"])
    
    # Extraire des features temporelles utiles
    df["pickup_hour"] = df["pickup_datetime"].dt.hour
    df["dropoff_hour"] = df["dropoff_datetime"].dt.hour

    # Supprimer les colonnes originales datetime
    df = df.drop(columns=["pickup_datetime", "dropoff_datetime"], errors="ignore")
    
    # Convertir 'store_and_fwd_flag' en numérique (0 = 'N', 1 = 'Y')
    df["store_and_fwd_flag"] = df["store_and_fwd_flag"].map({"N": 0, "Y": 1})

    # Vérifier que toutes les colonnes sont bien numériques
    print("Types de données après transformation :")
    print(df.dtypes)

    return df
