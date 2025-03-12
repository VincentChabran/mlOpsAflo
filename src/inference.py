import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import joblib
import pandas as pd
import yaml
from src.utils import load_data  
from src.preprocessing import preprocess_data 


# Charger la configuration
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

# Charger le modèle
model = joblib.load(config["model_path"])

df_test = load_data("test")  # On charge les données de test

# Appliquer le même prétraitement que pour l'entraînement
df_test = preprocess_data(df_test)

# Vérifier que toutes les features sont bien présentes avant de prédire
expected_features = [
    "vendor_id", "passenger_count", "pickup_longitude", "pickup_latitude",
    "dropoff_longitude", "dropoff_latitude", "store_and_fwd_flag",
    "pickup_hour", "dropoff_hour"
]

missing_features = [feat for feat in expected_features if feat not in df_test.columns]
if missing_features:
    print(f"⚠️ Attention : Les colonnes suivantes sont manquantes et seront ajoutées avec 0 : {missing_features}")
    for feat in missing_features:
        df_test[feat] = 0  # Valeur par défaut pour les colonnes manquantes

# Faire des prédictions sur toutes les lignes du fichier de test
predictions = model.predict(df_test)

# Ajouter les prédictions aux données
df_test["predicted_trip_duration"] = predictions


# Enregistrer les résultats dans un fichier CSV
df_test.to_csv("data/predictions.csv", index=False)

print("✅ Les prédictions ont été enregistrées dans data/predictions.csv")

# Afficher les premières prédictions
print("Prédictions sur un échantillon de test :")
print(predictions[:5])
