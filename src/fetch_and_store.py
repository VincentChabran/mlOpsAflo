import os
import requests
import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from src.utils import DB_PATH  # Import du prétraitement
import yaml


# Définir les chemins
ZIP_URL = "https://github.com/eishkina-estia/ML2023/raw/main/data/New_York_City_Taxi_Trip_Duration.zip"
ZIP_PATH = "data/nyc_taxi.zip"
TABLE_TRAIN = "train_data"
TABLE_TEST = "test_data"


# Charger la config
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)


# 🔹 Étape 1 : Télécharger les données avec requests
def download_data():
    if not os.path.exists("data"):
        os.makedirs("data")
    
    if not os.path.exists(ZIP_PATH):
        print("📥 Téléchargement des données depuis Kaggle...")
        response = requests.get(ZIP_URL, stream=True)
        with open(ZIP_PATH, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print("✅ Téléchargement terminé !")
    else:
        print("✔️ Les données existent déjà, pas besoin de télécharger.")


# 🔹 Étape 2 : Charger et prétraiter les données
def load_and_split_data():
    print("📂 Extraction et chargement des données...")

    # Lire directement le fichier ZIP
    df = pd.read_csv(ZIP_PATH, compression="zip")

    # Vérifier les colonnes disponibles
    print("🔎 Colonnes disponibles :", df.columns.tolist())

    # Séparer X (features) et y (target)
    X = df.drop(columns=["trip_duration"])
    y = df["trip_duration"]

    # Split des données en 70% train et 30% test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=config["random_state"]
    )

    print(f"✅ Données divisées : Train ({len(X_train)}) | Test ({len(X_test)})")
    
    return X_train, X_test, y_train, y_test


# 🔹 Étape 3 : Sauvegarder dans SQLite
def save_to_sqlite(X_train, X_test, y_train, y_test):
    print("📦 Sauvegarde des données dans la base SQLite...")

    conn = sqlite3.connect(DB_PATH)

    # Fusionner X et y avant sauvegarde
    train_data = X_train.copy()
    train_data["trip_duration"] = y_train

    test_data = X_test.copy()
    test_data["trip_duration"] = y_test

    # Sauvegarde dans SQLite
    train_data.to_sql(TABLE_TRAIN, conn, if_exists="replace", index=False)
    test_data.to_sql(TABLE_TEST, conn, if_exists="replace", index=False)

    conn.close()
    print(f"✅ Données enregistrées dans {DB_PATH} : {TABLE_TRAIN} & {TABLE_TEST}")


# 🔹 Exécuter tout le pipeline
if __name__ == "__main__":
    download_data()
    X_train, X_test, y_train, y_test = load_and_split_data()
    save_to_sqlite(X_train, X_test, y_train, y_test)
    print("🚀 Pipeline terminé avec succès !")
