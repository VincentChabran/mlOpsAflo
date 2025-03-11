#!/bin/bash

echo "🚀 Exécution du pipeline complet..."

# Étape 1 : Activer l'environnement Conda
echo "🔄 Activation de l'environnement Conda..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate nyc_taxi

# Étape 2 : Télécharger et stocker les données dans SQLite
echo "📥 Téléchargement et stockage des données..."
python src/fetch_and_store.py

# Étape 3 : Entraîner le modèle
echo "📊 Entraînement du modèle..."
python src/train.py

# Étape 4 : Lancer l'inférence
echo "🤖 Exécution de l'inférence..."
python src/inference.py

echo "✅ Pipeline terminé avec succès ! 🎉"
