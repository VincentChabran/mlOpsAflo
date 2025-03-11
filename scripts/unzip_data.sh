#!/bin/bash

echo "📂 Extraction des données..."

# Vérifier si le dossier data existe
if [ ! -d "data" ]; then
    echo "❌ Dossier 'data/' introuvable !"
    exit 1
fi

# Extraire tous les fichiers ZIP
for file in data/*.zip
do
    echo "📦 Extraction de $file..."
    unzip -o "$file" -d data/
done

echo "✅ Extraction terminée !"
