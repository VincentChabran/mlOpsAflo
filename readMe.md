# 🚕 NYC Taxi Trip Duration Prediction

Ce projet prédit la durée des trajets en taxi à New York en utilisant des modèles de Machine Learning. Il est entièrement automatisé avec des scripts Bash.

---

## 📂 **Architecture du projet**

```
nyc_taxi_trip/
│── data/                     # 📂 Données brutes et prédictions
│   ├── train.csv              # 📄 Données d'entraînment
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
│── src/                        # 📂 Code source du projet
│   ├── preprocessing.py        # 🔄 Nettoyage et transformation des données
│   ├── train.py                # 🎯 Entraînement du modèle
│   ├── inference.py            # 🔍 Prédictions sur les nouvelles données
│
│── scripts/                    # 📂 Scripts d'automatisation
│   ├── setup.sh                # 🛠 Installation des dépendances et environnement
│   ├── unzip_data.sh           # 📂 Extraction des données
│   ├── run_pipeline.sh         # 🚀 Entraînement et inférence automatique
│   ├── run_all.sh              # 🔄 Exécute tout le pipeline
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
chmod +x setup.sh
./setup.sh
```

Si l'environnement existe déjà, il ne sera pas recréé.

### 📂 **3. Extraire les données**

```bash
chmod +x unzip_data.sh
./unzip_data.sh
```

### 🎯 **4. Entraîner le modèle et exécuter l'inférence**

```bash
chmod +x run_pipeline.sh
./run_pipeline.sh
```

# OU pour tout exécuter en une seule commande :

```bash
chmod +x run_all.sh
./run_all.sh
```

---

## 📊 **Exploration des données**

Si vous souhaitez analyser les données avant l'entraînement, ouvrez le notebook :

```bash
jupyter notebook notebooks/EDA.ipynb
```

---

## 🔍 **Fichiers principaux et leur rôle**

| Fichier            | Description                                          |
| ------------------ | ---------------------------------------------------- |
| `train.py`         | Entraîne le modèle de prédiction                     |
| `inference.py`     | Prédit la durée des trajets sur de nouvelles données |
| `preprocessing.py` | Nettoie et prépare les données pour l'entraînement   |
| `setup.sh`         | Installe l'environnement et les dépendances          |
| `unzip_data.sh`    | Décompresse les données ZIP                          |
| `run_pipeline.sh`  | Lance l'entraînement et l'inférence                  |
| `run_all.sh`       | Exécute tout le pipeline d'un coup                   |

---

## 📌 **Améliorations possibles**

-  🔄 **Optimisation du modèle** : Essayer d'autres algorithmes (XGBoost, LGBM, etc.)
-  🚀 **Déploiement en API** : Utiliser Flask ou FastAPI pour prédire en temps réel
-  🔍 **Visualisation avancée** : Analyser les résultats dans un dashboard Streamlit

---

## 📞 **Support et contact**

Si vous avez des questions, ouvrez une issue sur le repo GitHub ! 😊

🎯 **Bon Machine Learning !** 🚀
# mlOpsAflo
