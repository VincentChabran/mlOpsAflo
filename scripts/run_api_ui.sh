#!/bin/bash

echo "🚀 Démarrage de l'API et de l'UI..."

# Étape 1 : Vérifier et configurer l'environnement Conda
echo "🔧 Vérification et configuration de l'environnement..."
bash scripts/setup_env.sh

# Étape 2 : Activer l'environnement Conda
echo "🔄 Activation de l'environnement Conda..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate nyc_taxi

# Étape 3 : Lancer l'API FastAPI
echo "🌍 Démarrage de l'API FastAPI..."
bash scripts/start_api.sh &  # Exécuter en arrière-plan

# Étape 4 : Attendre quelques secondes pour s'assurer que l'API démarre
sleep 5

# Étape 5 : Lancer l'interface Streamlit
echo "🖥 Lancement de l'interface utilisateur Streamlit..."
bash scripts/start_ui.sh &  # Exécuter en arrière-plan

echo "✅ L'API et l'UI sont en cours d'exécution !"
echo "📌 API disponible sur : http://localhost:8000/docs"
echo "📌 Interface UI disponible sur : http://localhost:8501"
