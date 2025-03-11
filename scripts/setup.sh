#!/bin/bash

echo "🚀 Initialisation du projet NYC Taxi Trip..."

# Vérifier que Conda est installé
if ! command -v conda &> /dev/null
then
    echo "❌ Conda n'est pas installé. Installe-le avant de continuer."
    exit 1
fi

# Vérifier si l'environnement 'nyc_taxi' existe déjà
if conda env list | grep -q "nyc_taxi"; then
    echo "✅ L'environnement 'nyc_taxi' existe déjà. Activation..."
else
    echo "📦 Création de l'environnement Conda..."
    conda create --name nyc_taxi python=3.11 -y
fi

# Activer l'environnement
echo "🔄 Activation de l'environnement Conda..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate nyc_taxi

# Installer les dépendances (sans réinstaller ce qui est déjà présent)
echo "📦 Installation des dépendances..."
pip install --upgrade --requirement requirements.txt

echo "✅ Installation terminée !"
