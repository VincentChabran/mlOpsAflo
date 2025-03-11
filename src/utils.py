import sqlite3
import pandas as pd

DB_PATH = "data/nyc_taxi.db"

def load_data(data_type="train"):
    """
    Charge les données depuis la base SQLite.
    
    - `data_type="train"` → charge les données d'entraînement.
    - `data_type="test"` → charge les données de test.

    Retourne un DataFrame pandas.
    """
    table_name = "train_data" if data_type == "train" else "test_data"

    print(f"📥 Chargement des données ({data_type}) depuis SQLite...")

    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()

    print(f"✅ Données chargées : {len(df)} lignes récupérées.")
    return df
