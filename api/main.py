import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yaml
import sqlite3
from src.TaxiTripModel import TaxiTripModel

# Charger la configuration
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

# Initialiser le modèle
model = TaxiTripModel()

# Initialiser l'application FastAPI
app = FastAPI(title="NYC Taxi Trip Prediction API")


# Définition du schéma de requête
class TripRequest(BaseModel):
    pickup_datetime: str
    vendor_id: int
    passenger_count: int
    pickup_longitude: float
    pickup_latitude: float
    dropoff_longitude: float
    dropoff_latitude: float
    store_and_fwd_flag: int


@app.get("/")
def root():
    return {"message": "🚖 Bienvenue sur l'API NYC Taxi Trip Prediction !"}


@app.post("/predict")
def predict_trip_duration(request: TripRequest):
    """
    Endpoint pour faire une prédiction sur la durée du trajet et estimer `dropoff_datetime`.
    """
    try:
        # Convertir l'entrée utilisateur en dictionnaire
        input_data = request.dict()

        # Faire la prédiction avec la méthode `predict_single_trip`
        prediction_result = model.predict_single_trip(input_data)

        return {
            "predicted_trip_duration": prediction_result["predicted_trip_duration"],
            "estimated_dropoff_datetime": prediction_result["estimated_dropoff_datetime"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Erreur lors de la prédiction : {str(e)}")


@app.get("/predictions")
def get_predictions():
    """
    Récupère toutes les prédictions enregistrées dans la base de données.
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
                "weekday": row[9],
                "dropoff_hour": row[10],
                "predicted_trip_duration": row[11]
            }
            for row in rows
        ]

        return {"predictions": predictions_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Erreur lors de la récupération des prédictions : {str(e)}")


# ✅ Lancer l'API avec Uvicorn
if __name__ == '__main__':
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
