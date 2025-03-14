import sqlite3
import pandas as pd
import joblib
import numpy as np
import yaml
from sklearn.ensemble import RandomForestRegressor


class TaxiTripModel:
    def __init__(self, config_path="config.yml"):
        """Initialise le modèle avec les paramètres du fichier de configuration."""
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        self.db_path = self.config["db_path"]
        self.model_path = self.config["model_path"]

        # Charger le modèle s'il existe, sinon créer un nouveau modèle
        try:
            self.model = joblib.load(self.model_path)
            print(f"🔮 Modèle chargé depuis {self.model_path}")
        except FileNotFoundError:
            self.model = RandomForestRegressor(n_estimators=10, max_depth=5, random_state=42)
            print(f"⚠️ Modèle non trouvé, un nouveau modèle sera entraîné.")

    def preprocess_data(self, df, is_train=False):
        """
        Nettoie et transforme les données.
        - is_train=True : conserve `trip_duration` et applique la transformation logarithmique.
        - is_train=False : supprime `trip_duration` pour l'inférence.
        """

        # Supprimer la colonne 'id' si présente
        df = df.drop(columns=["id"], errors="ignore")

        # Convertir 'pickup_datetime' et extraire les features temporelles
        if "pickup_datetime" in df.columns:
            df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"])
            df["pickup_hour"] = df["pickup_datetime"].dt.hour
            df["weekday"] = df["pickup_datetime"].dt.weekday  # 0 = lundi, 6 = dimanche
            df = df.drop(columns=["pickup_datetime"], errors="ignore")

        # Convertir 'dropoff_datetime' et extraire l'heure de dépose
        if "dropoff_datetime" in df.columns:
            df["dropoff_datetime"] = pd.to_datetime(df["dropoff_datetime"])
            df["dropoff_hour"] = df["dropoff_datetime"].dt.hour
            df = df.drop(columns=["dropoff_datetime"], errors="ignore")
        else:
            df["dropoff_hour"] = 0  # Ajout d'une valeur par défaut

        # Convertir 'store_and_fwd_flag' en numérique
        if "store_and_fwd_flag" in df.columns:
            df["store_and_fwd_flag"] = df["store_and_fwd_flag"].map({"N": 0, "Y": 1})

        # Transformation logarithmique de `trip_duration`
        if is_train and "trip_duration" in df.columns:
            df["log_trip_duration"] = np.log1p(df["trip_duration"])

        # Supprimer `trip_duration` pour l'inférence
        if not is_train:
            df = df.drop(columns=["trip_duration"], errors="ignore")

        return df

    def train(self):
        """Charge les données d'entraînement, applique le prétraitement et entraîne le modèle."""

        # 📥 Charger les données d'entraînement depuis la base SQLite
        conn = sqlite3.connect(self.db_path)
        df_train = pd.read_sql("SELECT * FROM train_data", conn)
        conn.close()

        print(f"📊 Colonnes AVANT prétraitement (train) : {df_train.columns.tolist()}")

        # 🔄 Appliquer le prétraitement
        df_train = self.preprocess_data(df_train, is_train=True)

        print(f"📊 Colonnes APRÈS prétraitement (train) : {df_train.columns.tolist()}")

        # Séparer features et target
        y_train = df_train["log_trip_duration"]
        X_train = df_train.drop(columns=["log_trip_duration"], errors="ignore")

        # 📊 Entraîner le modèle
        print("📊 Début de l'entraînement du modèle...")
        self.model.fit(X_train, y_train)
        print("✅ Entraînement terminé.")

        # 🔄 Sauvegarder le modèle
        joblib.dump(self.model, self.model_path)
        print(f"✅ Modèle enregistré dans {self.model_path} 🎯")

    def predict_from_sql(self):
        """Charge les données de test depuis SQLite, applique le prétraitement et fait des prédictions."""

        # 📥 Charger les données de test depuis SQLite
        conn = sqlite3.connect(self.db_path)
        df_test = pd.read_sql("SELECT * FROM test_data", conn)
        conn.close()

        print(f"🔍 Colonnes AVANT prétraitement (inférence) : {df_test.columns.tolist()}")

        # 🔄 Appliquer le prétraitement
        df_test = self.preprocess_data(df_test, is_train=False)

        print(f"🔍 Colonnes APRÈS prétraitement (inférence) : {df_test.columns.tolist()}")

        # 🔮 Faire les prédictions
        log_predictions = self.model.predict(df_test)

        # 🎯 Reconvertir en secondes
        df_test["predicted_trip_duration"] = np.expm1(log_predictions)

        # 📦 Sauvegarder en base
        self.save_predictions_to_db(df_test)

        return df_test

    def save_predictions_to_db(self, df):
        """Sauvegarde les prédictions dans la base de données SQLite."""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Vérifier que la table `predictions` existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vendor_id INTEGER,
                passenger_count INTEGER,
                pickup_longitude REAL,
                pickup_latitude REAL,
                dropoff_longitude REAL,
                dropoff_latitude REAL,
                store_and_fwd_flag INTEGER,
                pickup_hour INTEGER,
                weekday INTEGER,
                dropoff_hour INTEGER,
                predicted_trip_duration REAL
            )
        ''')

        # Insérer les prédictions dans la table
        for _, row in df.iterrows():
            cursor.execute('''
                INSERT INTO predictions (
                    vendor_id, passenger_count, pickup_longitude, pickup_latitude,
                    dropoff_longitude, dropoff_latitude, store_and_fwd_flag,
                    pickup_hour, weekday, dropoff_hour, predicted_trip_duration
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row["vendor_id"], row["passenger_count"], row["pickup_longitude"], row["pickup_latitude"],
                row["dropoff_longitude"], row["dropoff_latitude"], row["store_and_fwd_flag"],
                row["pickup_hour"], row["weekday"], row["dropoff_hour"], row["predicted_trip_duration"]
            ))

        conn.commit()
        conn.close()

        print(f"✅ Prédictions sauvegardées dans SQLite ({self.db_path})")

    def predict_single_trip(self, trip_data):
        """Prédit la durée d'un trajet unique à partir d'une entrée utilisateur."""
        df = pd.DataFrame([trip_data])
        
        # 🔄 Appliquer le prétraitement
        df = self.preprocess_data(df, is_train=False)

        # 🔮 Faire la prédiction
        log_prediction = self.model.predict(df)[0]

        # 🎯 Reconvertir en secondes
        predicted_duration = np.expm1(log_prediction)

        # Ajouter `dropoff_datetime` estimé
        pickup_datetime = pd.to_datetime(trip_data["pickup_datetime"])
        dropoff_datetime = pickup_datetime + pd.to_timedelta(predicted_duration, unit="s")

        return {
            "predicted_trip_duration": predicted_duration,
            "estimated_dropoff_datetime": dropoff_datetime.strftime("%Y-%m-%d %H:%M:%S")
        }
