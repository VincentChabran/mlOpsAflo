#!/bin/bash

echo "🌍 Démarrage de l'API FastAPI..."

# Activer l'environnement Conda
source $(conda info --base)/etc/profile.d/conda.sh
conda activate nyc_taxi

# Lancer FastAPI avec Uvicorn
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
