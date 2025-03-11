import joblib
import pandas as pd
import yaml

# Charger la configuration
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

# Charger le modèle
model = joblib.load(config["model_path"])

# Charger les données de test
df_test = pd.read_csv("data/test.csv")

# Nettoyer les noms de colonnes (supprimer les espaces cachés)
df_test.columns = df_test.columns.str.strip()

# Vérifier les colonnes disponibles
print("Colonnes disponibles après nettoyage :", df_test.columns.tolist())

# Vérifier si 'pickup_datetime' est bien présent avant de l'utiliser
if "pickup_datetime" in df_test.columns:
    df_test["pickup_hour"] = pd.to_datetime(df_test["pickup_datetime"]).dt.hour
    df_test = df_test.drop(columns=["pickup_datetime"], errors="ignore")
else:
    print("⚠️ Attention : 'pickup_datetime' non trouvé dans les données de test !")

# Vérifier si 'dropoff_datetime' est présent avant de l'utiliser
if "dropoff_datetime" in df_test.columns:
    df_test["dropoff_hour"] = pd.to_datetime(df_test["dropoff_datetime"]).dt.hour
    df_test = df_test.drop(columns=["dropoff_datetime"], errors="ignore")
else:
    print("⚠️ Attention : 'dropoff_datetime' non trouvé dans les données de test !")
    df_test["dropoff_hour"] = 0  # Ajout d'une colonne factice pour éviter l'erreur

# Convertir 'store_and_fwd_flag' en variable numérique (0 = 'N', 1 = 'Y')
if "store_and_fwd_flag" in df_test.columns:
    df_test["store_and_fwd_flag"] = df_test["store_and_fwd_flag"].map({"N": 0, "Y": 1})

# Supprimer la colonne 'id' (inutile pour la prédiction)
df_test = df_test.drop(columns=["id"], errors="ignore")

# Vérifier si toutes les colonnes sont bien numériques avant la prédiction
print("Types de données après prétraitement :")
print(df_test.dtypes)

# Vérifier que toutes les features sont bien présentes avant de prédire
expected_features = [
    "vendor_id", "passenger_count", "pickup_longitude", "pickup_latitude",
    "dropoff_longitude", "dropoff_latitude", "store_and_fwd_flag",
    "pickup_hour", "dropoff_hour"
]

missing_features = [feat for feat in expected_features if feat not in df_test.columns]
if missing_features:
    print(f"⚠️ Attention : Les colonnes suivantes sont manquantes et seront ajoutées avec 0 : {missing_features}")
    for feat in missing_features:
        df_test[feat] = 0  # Valeur par défaut pour les colonnes manquantes

# Faire des prédictions sur toutes les lignes du fichier de test
predictions = model.predict(df_test)

# Ajouter les prédictions aux données
df_test["predicted_trip_duration"] = predictions

# Enregistrer les résultats dans un fichier CSV
df_test.to_csv("data/predictions.csv", index=False)

print("✅ Les prédictions ont été enregistrées dans data/predictions.csv")

# Afficher les premières prédictions
print("Prédictions sur un échantillon de test :")
print(predictions[:5])
