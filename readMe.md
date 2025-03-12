# 🚕 NYC Taxi Trip Duration Prediction

Ce projet prédit la durée des trajets en taxi à New York en utilisant des modèles de Machine Learning. Il est entièrement automatisé avec des scripts Bash et propose une API FastAPI ainsi qu'une interface utilisateur Streamlit.

---

## 📂 **Architecture du projet**

```
nyc_taxi_trip/
│── api/                      # 📂 Code source de l'API FastAPI
│   ├── main.py               # 🌍 API pour servir les prédictions
│
│── data/                     # 📂 Données brutes et prédictions
│   ├── train.csv              # 📄 Données d'entraînement
│   ├── test.csv               # 📄 Données de test
│   ├── predictions.csv        # 📄 Résultats des prédictions
│   ├── nyc_taxi.zip           # 📦 Archive des données (optionnel)
│
│── models/                    # 📂 Modèles entraînés
│   ├── taxi_model.pkl         # 🤖 Modèle sauvegardé
│
│── notebooks/                  # 📂 Analyses exploratoires
│   ├── EDA.ipynb              # 📊 Notebook d'analyse des données
│
│── scripts/                    # 📂 Scripts d'automatisation
│   ├── setup_env.sh            # 🛠 Installation des dépendances et environnement
│   ├── extract_data.sh         # 📂 Extraction des données et stockage SQLite
│   ├── train_model.sh          # 🎯 Entraînement du modèle
│   ├── run_inference.sh        # 🤖 Exécution de l'inférence
│   ├── start_api.sh            # 🌍 Démarrage de FastAPI
│   ├── start_ui.sh             # 🖥 Démarrage de Streamlit UI
│   ├── run_ml_pipeline.sh      # 🚀 Exécute tout le pipeline Machine Learning
│   ├── run_api_ui.sh           # 🌎 Démarre l’API et l’UI en parallèle
│
│── src/                        # 📂 Code source du projet
│   ├── fetch_and_store.py      # 🗄 Stockage des données dans SQLite
│   ├── preprocessing.py        # 🔄 Nettoyage et transformation des données
│   ├── train.py                # 🎯 Entraînement du modèle
│   ├── inference.py            # 🔍 Prédictions sur les nouvelles données
│   ├── utils.py                # 🛠 Fonctions utilitaires
│
│── ui/                         # 📂 Interface utilisateur avec Streamlit
│   ├── app.py                  # 🖥 Interface web utilisateur
│
│── config.yml                  # ⚙️ Configuration du projet
│── requirements.txt             # 📦 Dépendances Python
│── README.md                    # 📖 Documentation du projet
```

---

## 🚀 **Comment exécuter le projet ?**

### 📌 **Prérequis**

-  **Python 3.11+**
-  **Conda** (installé via [Miniconda](https://docs.conda.io/en/latest/miniconda.html))
-  **Git**

### 📥 **1. Cloner le repo et entrer dans le dossier**

```bash
git clone https://github.com/ton-user/nyc_taxi_trip.git
cd nyc_taxi_trip
```

### 🛠 **2. Installer l'environnement et les dépendances**

```bash
bash scripts/setup_env.sh
```

Si l'environnement existe déjà, il ne sera pas recréé.

### 📂 **3. Extraire les données et les stocker dans SQLite**

```bash
bash scripts/extract_data.sh
```

### 🎯 **4. Entraîner le modèle et exécuter l'inférence**

```bash
bash scripts/run_ml_pipeline.sh
```

### 🌍 **5. Lancer l'API et l'interface utilisateur**

```bash
bash scripts/run_api_ui.sh
```

---

## 📊 **Exploration des données**

Si vous souhaitez analyser les données avant l'entraînement, ouvrez le notebook :

```bash
jupyter notebook notebooks/EDA.ipynb
```

---

## 🔍 **Fichiers principaux et leur rôle**

| Fichier              | Description                                          |
| -------------------- | ---------------------------------------------------- |
| `train.py`           | Entraîne le modèle de prédiction                     |
| `inference.py`       | Prédit la durée des trajets sur de nouvelles données |
| `fetch_and_store.py` | Stocke les données dans SQLite                       |
| `preprocessing.py`   | Nettoie et prépare les données pour l'entraînement   |
| `setup_env.sh`       | Installe l'environnement et les dépendances          |
| `extract_data.sh`    | Décompresse les données ZIP et stocke dans SQLite    |
| `run_ml_pipeline.sh` | Exécute tout le pipeline Machine Learning            |
| `run_api_ui.sh`      | Démarre l’API et l’interface utilisateur             |

---

## 📌 **Améliorations possibles**

-  🔄 **Optimisation du modèle** : Essayer d'autres algorithmes (XGBoost, LGBM, etc.)
-  🚀 **Déploiement en production** : Héberger l'API sur un serveur cloud
-  🔍 **Ajout de monitoring** : Suivi des performances en temps réel

---

## 📞 **Support et contact**

Si vous avez des questions, ouvrez une issue sur le repo GitHub ! 😊

🎯 **Bon Machine Learning !** 🚀
