#!/bin/bash

echo "🤖 Exécution de l'inférence..."

# Activer l'environnement Conda
source $(conda info --base)/etc/profile.d/conda.sh
conda activate nyc_taxi

# Exécuter l’inférence
python src/inference.py

echo "✅ Inférence terminée ! 🔮"
