import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.TaxiTripModel import TaxiTripModel
import sqlite3
import yaml
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor

# Charger la config
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

DB_PATH = config["db_path"]

# Charger les données
conn = sqlite3.connect(DB_PATH)
df_train = pd.read_sql("SELECT * FROM train_data", conn)
conn.close()

# Créer une instance du modèle
model = TaxiTripModel()

# Appliquer le prétraitement (avec `log_trip_duration`)
df_train = model.preprocess_data(df_train, is_train=True)

# Définir les features et la target
y_train = df_train["log_trip_duration"]
X_train = df_train.drop(columns=["trip_duration", "log_trip_duration"], errors="ignore")

# Définir et entraîner le modèle
model_rf = RandomForestRegressor(n_estimators=10, max_depth=5, random_state=42)
model_rf.fit(X_train, y_train)

# Sauvegarder le modèle
joblib.dump(model_rf, config["model_path"])
print("✅ Modèle entraîné et sauvegardé 🎯")
