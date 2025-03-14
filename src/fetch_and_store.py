import os
import requests
import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
import yaml
import zipfile
import glob

# Charger la configuration depuis config.yml
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

# Utiliser les valeurs du fichier de configuration
DATA_URL = config["data_url"]
ZIP_PATH = config["zip_path"]
CSV_PATH = config["csv_train_path"]
DB_PATH = config["db_path"]
TABLE_TRAIN = config["table_train"]
TABLE_TEST = config["table_test"]
TEST_SIZE = config["test_size"]
RANDOM_STATE = config["random_state"]

# 🔹 Étape 1 : Télécharger les données
def download_data():
    """Télécharge le fichier ZIP si non présent"""
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(ZIP_PATH):
        print("📥 Téléchargement des données...")
        response = requests.get(DATA_URL, stream=True)
        with open(ZIP_PATH, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print("✅ Téléchargement terminé !")
    else:
        print("✔️ Le fichier ZIP existe déjà.")


# 🔹 Étape 2 : Extraire les données si nécessaire
def extract_data():
    """Extrait le fichier ZIP et trouve automatiquement le fichier CSV à utiliser."""
    if not os.path.exists(CSV_PATH):
        print("📂 Extraction des données...")

        # Extraire le fichier ZIP
        with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
            zip_ref.extractall("data/")

        # Trouver automatiquement le fichier CSV extrait
        extracted_files = glob.glob("data/*.csv")
        if extracted_files:
            extracted_file = extracted_files[0]  # Prendre le premier fichier CSV trouvé
            os.rename(extracted_file, CSV_PATH)
            print(f"✅ Fichier extrait et renommé en {CSV_PATH}")
        else:
            print("❌ Erreur : Aucun fichier CSV trouvé après extraction !")
            exit(1)
    else:
        print("✔️ Données déjà extraites.")




# 🔹 Étape 3 : Charger et afficher un aperçu des données
def load_and_preview_data():
    """Charge les données et affiche un aperçu"""
    print("📥 Chargement des données...")
    df = pd.read_csv(CSV_PATH)

    print("\n🔎 Aperçu des premières lignes :")
    print(df.head())

    print("\n📊 Types des colonnes :")
    print(df.dtypes)

    print("\n🔎 Valeurs manquantes par colonne :")
    print(df.isna().sum())

    return df


# 🔹 Étape 4 : Split des données en `train` et `test`
def split_data(df):
    """Sépare les données en train et test"""
    print("\n📊 Division des données en train et test...")

    X = df.drop(columns=["trip_duration"])
    y = df["trip_duration"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )

    print(f"✅ Données divisées : Train ({len(X_train)}) | Test ({len(X_test)})")
    return X_train, X_test, y_train, y_test


# 🔹 Étape 5 : Sauvegarder les données dans SQLite
def save_to_sqlite(X_train, X_test, y_train, y_test):
    """Sauvegarde les datasets train et test dans la base de données SQLite"""
    print("\n📦 Sauvegarde des données dans SQLite...")

    conn = sqlite3.connect(DB_PATH)

    train_data = X_train.copy()
    train_data["trip_duration"] = y_train

    test_data = X_test.copy()
    test_data["trip_duration"] = y_test

    train_data.to_sql(TABLE_TRAIN, conn, if_exists="replace", index=False)
    test_data.to_sql(TABLE_TEST, conn, if_exists="replace", index=False)

    conn.close()
    print(f"✅ Données enregistrées dans {DB_PATH} : {TABLE_TRAIN} & {TABLE_TEST}")


# 🔹 Exécution du pipeline complet
if __name__ == "__main__":
    download_data()       # Étape 1 : Télécharger
    extract_data()        # Étape 2 : Extraire
    df = load_and_preview_data()  # Étape 3 : Charger et afficher
    X_train, X_test, y_train, y_test = split_data(df)  # Étape 4 : Split
    save_to_sqlite(X_train, X_test, y_train, y_test)  # Étape 5 : Sauvegarde

    print("\n🚀 Pipeline terminé avec succès ! 🎉")
