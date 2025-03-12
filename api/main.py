import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
from pydantic import BaseModel
import uvicorn
import sqlite3
import yaml
from src.utils import create_predictions_table
from src.preprocessing import preprocess_data

# Charger la configuration depuis config.yml
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

# Charger le modèle depuis le chemin de configuration
MODEL_PATH = config["model_path"]
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"❌ Erreur lors du chargement du modèle : {str(e)}")

# Initialiser l'application FastAPI
app = FastAPI(title="NYC Taxi Trip Prediction API")

# Vérifier que la table SQLite `predictions` est bien créée
create_predictions_table()


class TripRequest(BaseModel):
    vendor_id: int
    passenger_count: int
    pickup_longitude: float
    pickup_latitude: float
    dropoff_longitude: float
    dropoff_latitude: float
    store_and_fwd_flag: int
    pickup_hour: int  # ✅ On garde seulement pickup_hour (dropoff_hour sera généré)


@app.get("/")
def root():
    return {"message": "🚖 Bienvenue sur l'API de prédiction NYC Taxi Trip !"}


@app.post("/predict")
def predict_trip_duration(request: TripRequest):
    """
    Endpoint pour faire une prédiction et sauvegarder le résultat en base de données.
    """
    try:
        # Convertir l'entrée en DataFrame
        input_data = pd.DataFrame([request.dict()])

        # ✅ Appliquer le prétraitement (génère dropoff_hour)
        input_data = preprocess_data(input_data, is_train=False)

        # 🛠 Debugging pour voir les colonnes et types
        print("🌍 Colonnes APRÈS prétraitement (API) :", input_data.columns.tolist())
        print("🔍 Types des colonnes après prétraitement (API) :\n", input_data.dtypes)
        print("🔍 Vérification des valeurs manquantes (API) :\n", input_data.isna().sum())

        # Vérifier si NaN avant la prédiction
        if input_data.isna().sum().sum() > 0:
            raise HTTPException(status_code=400, detail="❌ Données d'entrée invalides : présence de NaN après prétraitement.")

        # Faire la prédiction
        prediction = model.predict(input_data)[0]

        # Sauvegarder dans SQLite
        conn = sqlite3.connect(config["db_path"])
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO predictions (vendor_id, passenger_count, pickup_longitude, pickup_latitude,
                                     dropoff_longitude, dropoff_latitude, store_and_fwd_flag,
                                     pickup_hour, dropoff_hour, predicted_trip_duration)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            request.vendor_id, request.passenger_count, request.pickup_longitude, request.pickup_latitude,
            request.dropoff_longitude, request.dropoff_latitude, request.store_and_fwd_flag,
            request.pickup_hour, input_data["dropoff_hour"].iloc[0], prediction  # ✅ dropoff_hour ajouté
        ))

        conn.commit()
        conn.close()

        return {"predicted_trip_duration": prediction, "message": "Prédiction enregistrée en base"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction : {str(e)}")



@app.get("/predictions")
def get_predictions():
    """
    📊 Récupère toutes les prédictions enregistrées en base de données.
    """
    try:
        conn = sqlite3.connect(config["db_path"])
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM predictions ORDER BY id DESC")
        rows = cursor.fetchall()

        conn.close()

        # Construire la réponse sous forme de liste de dictionnaires
        predictions_list = [
            {
                "id": row[0],
                "vendor_id": row[1],
                "passenger_count": row[2],
                "pickup_longitude": row[3],
                "pickup_latitude": row[4],
                "dropoff_longitude": row[5],
                "dropoff_latitude": row[6],
                "store_and_fwd_flag": row[7],
                "pickup_hour": row[8],
                "predicted_trip_duration": row[9]  # ⚠️ Indice mis à jour
            }
            for row in rows
        ]

        return {"predictions": predictions_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Erreur lors de la récupération des prédictions : {str(e)}")


# ✅ Lancer l'API avec Uvicorn
if __name__ == '__main__':
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
