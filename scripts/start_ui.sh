#!/bin/bash

echo "🖥 Lancement de l'interface Streamlit..."

# Activer l'environnement Conda
source $(conda info --base)/etc/profile.d/conda.sh
conda activate nyc_taxi

# Lancer Streamlit
streamlit run ui/app.py --server.port 8501 --server.address 0.0.0.0
