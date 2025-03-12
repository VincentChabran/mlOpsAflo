import sqlite3
import pandas as pd
import yaml


with open("config.yml", "r") as f:
    config = yaml.safe_load(f)


def load_data(data_type="train"):
    """
    Charge les données depuis la base SQLite.
    
    - `data_type="train"` → charge les données d'entraînement.
    - `data_type="test"` → charge les données de test.

    Retourne un DataFrame pandas.
    """
    table_name = "train_data" if data_type == "train" else "test_data"

    print(f"📥 Chargement des données ({data_type}) depuis SQLite...")

    conn = sqlite3.connect(config["db_path"])
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()

    print(f"✅ Données chargées : {len(df)} lignes récupérées.")
    return df



def create_predictions_table():
    """Crée la table `predictions` si elle n'existe pas."""
    conn = sqlite3.connect(config["db_path"])
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor_id INTEGER,
            passenger_count INTEGER,
            pickup_longitude REAL,
            pickup_latitude REAL,
            dropoff_longitude REAL,
            dropoff_latitude REAL,
            store_and_fwd_flag INTEGER,
            pickup_hour INTEGER,
            dropoff_hour INTEGER,
            predicted_trip_duration REAL
        )
    ''')

    conn.commit()
    conn.close()

    print("✅ Table `predictions` vérifiée/créée dans SQLite.")
