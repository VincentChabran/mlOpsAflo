#!/bin/bash

echo "🚀 Exécution complète du pipeline Machine Learning..."

# Étape 1 : Activer l'environnement Conda et installer les dépendances
echo "🔧 Configuration de l'environnement..."
bash scripts/setup_env.sh

# Étape 2 : Extraire les données et stocker dans SQLite
echo "📂 Extraction des données et stockage dans SQLite..."
bash scripts/extract_data.sh

# Étape 3 : Entraîner le modèle
echo "📊 Entraînement du modèle..."
bash scripts/train_model.sh

# Étape 4 : Exécuter l'inférence
echo "🤖 Exécution de l'inférence..."
bash scripts/run_inference.sh

echo "✅ Pipeline Machine Learning terminé avec succès ! 🎉"
