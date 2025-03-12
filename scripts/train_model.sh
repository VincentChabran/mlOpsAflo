#!/bin/bash

echo "📊 Entraînement du modèle..."

# Activer l'environnement Conda
source $(conda info --base)/etc/profile.d/conda.sh
conda activate nyc_taxi

# Exécuter le script d'entraînement
python src/train.py

echo "✅ Modèle entraîné et sauvegardé ! 🎯"
