import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
from pydantic import BaseModel
import uvicorn
from src.utils import create_predictions_table
import yaml
import sqlite3


# Charger la config
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)


# Charger le modèle
MODEL_PATH = "models/taxi_model.pkl"
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Erreur lors du chargement du modèle : {str(e)}")

# Initialiser l'application FastAPI
app = FastAPI(title="NYC Taxi Trip Prediction API")

# Vérifier que la table SQLite est bien créée
create_predictions_table()


# Définir le schéma de l'entrée utilisateur
class TripRequest(BaseModel):
    vendor_id: int
    passenger_count: int
    pickup_longitude: float
    pickup_latitude: float
    dropoff_longitude: float
    dropoff_latitude: float
    store_and_fwd_flag: int
    pickup_hour: int
    dropoff_hour: int


@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API de prédiction de la durée des trajets en taxi NYC 🚖"}


@app.post("/predict")
def predict_trip_duration(request: TripRequest):
    """
    Endpoint pour faire une prédiction et sauvegarder le résultat en base de données.
    """
    try:
        # Convertir l'entrée en DataFrame
        input_data = pd.DataFrame([request.dict()])

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
            request.pickup_hour, request.dropoff_hour, prediction
        ))

        conn.commit()
        conn.close()

        return {"predicted_trip_duration": prediction, "message": "Prédiction enregistrée en base"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction : {str(e)}")


@app.get("/predictions")
def get_predictions():
    """
    Récupère toutes les prédictions enregistrées en base de données.
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
                "dropoff_hour": row[9],
                "predicted_trip_duration": row[10]
            }
            for row in rows
        ]

        return {"predictions": predictions_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des prédictions : {str(e)}")




if __name__ == '__main__':
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
