import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import joblib
import yaml
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from src.preprocessing import load_data, preprocess_data  # Import des fonctions

# Charger la config
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

# Charger et prétraiter les données
df = load_data(config["data_path"])
df = preprocess_data(df)

# Définir les features et la target
y = df["trip_duration"]
X = df.drop(columns=["trip_duration"], errors="ignore")  # Supprime la target du dataset

# Vérifier la structure des données après prétraitement
print("Aperçu des features après préprocessing :")
print(X.head())

# Séparer les données en train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=config["test_size"], random_state=config["random_state"]
)

# Définir et entraîner le modèle
model = RandomForestRegressor(n_estimators=10, max_depth=5, random_state=42)
print("Début de l'entraînement du modèle...")
model.fit(X_train, y_train)
print("Entraînement terminé.")

# Sauvegarder le modèle
joblib.dump(model, config["model_path"])
print(f"Modèle enregistré dans {config['model_path']}")
