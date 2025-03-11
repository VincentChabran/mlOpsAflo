#!/bin/bash

echo "🚀 Lancement du pipeline complet NYC Taxi Trip..."

chmod +x setup.sh unzip_data.sh run_pipeline.sh

# Étape 1 : Installation des dépendances et configuration
bash setup.sh

# Étape 2 : Extraction des données
bash unzip_data.sh

# Étape 3 : Entraînement du modèle et inférence
bash run_pipeline.sh

echo "✅ Tout le pipeline a été exécuté avec succès ! 🎉"
