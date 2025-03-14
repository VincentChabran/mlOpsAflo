import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.TaxiTripModel import TaxiTripModel

# Créer une instance du modèle
model = TaxiTripModel()

# Charger les données, faire l'inférence et sauvegarder les résultats
df_predictions = model.predict_from_sql()
print("✅ Prédictions terminées et stockées en base de données !")
