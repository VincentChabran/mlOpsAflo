import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import requests
import pandas as pd
import yaml

# Charger la configuration
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

API_URL = config["api_url"]  # Utiliser l'URL de l'API définie dans config.yml

# Configurer la page Streamlit
st.set_page_config(page_title="NYC Taxi Prediction", layout="centered")
st.title("🚖 NYC Taxi Trip Duration Prediction")

# Formulaire d'entrée utilisateur
st.sidebar.header("📝 Entrez les informations du trajet")

vendor_id = st.sidebar.selectbox("Vendor ID", [1, 2])
passenger_count = st.sidebar.number_input("Nombre de passagers", min_value=1, max_value=6, value=1)
pickup_longitude = st.sidebar.number_input("Longitude de départ", value=-73.985)
pickup_latitude = st.sidebar.number_input("Latitude de départ", value=40.748)
dropoff_longitude = st.sidebar.number_input("Longitude d'arrivée", value=-73.985)
dropoff_latitude = st.sidebar.number_input("Latitude d'arrivée", value=40.748)
store_and_fwd_flag = st.sidebar.selectbox("Store and Forward Flag", [0, 1])
pickup_hour = st.sidebar.slider("Heure de départ", 0, 23, 12)  # ✅ Garde uniquement pickup_hour

if st.sidebar.button("📊 Prédire la durée du trajet"):
    # Création du dictionnaire de données
    input_data = {
        "vendor_id": vendor_id,
        "passenger_count": passenger_count,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "store_and_fwd_flag": store_and_fwd_flag,
        "pickup_hour": pickup_hour  # ❌ Supprime dropoff_hour (calculé automatiquement)
    }

    # Envoi de la requête POST à l'API
    response = requests.post(f"{API_URL}/predict", json=input_data)

    if response.status_code == 200:
        result = response.json()
        st.success(f"⏳ Durée estimée du trajet : {result['predicted_trip_duration']} secondes")
    else:
        st.error("❌ Erreur lors de la prédiction. Vérifiez que l'API est bien lancée.")

# Section pour afficher les prédictions enregistrées
st.header("📊 Historique des prédictions")

if st.button("🔄 Rafraîchir l'historique"):
    response = requests.get(f"{API_URL}/predictions")

    if response.status_code == 200:
        data = response.json()["predictions"]
        df = pd.DataFrame(data)
        if not df.empty:
            st.dataframe(df)
        else:
            st.info("Aucune prédiction enregistrée.")
    else:
        st.error("❌ Erreur lors de la récupération des prédictions.")
