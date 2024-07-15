Ce projet a été réalisé dans le cadre de la formation Ingénieur IA (Intelligence Artificielle)  dispensée par Openclassroom. Cette formation se déroule sur 12 projets à réaliser. Ici est présenté le projet 8.
# OC_AIE_projet_8

## Systèmes de vision par ordinateur pour véhicules autonomes

### Contexte
Future Vision Transport conçoit des systèmes embarqués de vision par ordinateur pour les véhicules autonomes. Vous êtes un ingénieur IA au sein de l’équipe R&D, spécialisée dans la segmentation des images.

### Objectifs
- 🎯 Entraîner un modèle de segmentation des images sur les 8 catégories principales avec Keras..
    - 🔹 Approches avec des modèles simples mini_Unets et pré-entrainés : VGG16-Unet
- ☁️ Concevoir et déployer une API de prédiction (Flask) sur le Cloud (Azure) qui prend une image en entrée et renvoie le mask prédit.
- 🖥️ Créer et déployer une application web (Streamlit) pour tester l’API et afficher les résultats.
- 📝 Développer des scripts dans un notebook pour montrer la modélisation complète.
- 📝 Élaborer une note technique de 10 pages et un support de présentation pour illustrer votre démarche et vos résultats.

---

## Structure du Projet

Ce projet contient plusieurs répertoires et fichiers organisés comme suit :

### 📁 [.github](.github)
- [main_api-segmentation.yml](.github/workflows/main_api-segmentation.yml) : Workflow Github Actions pour l'api.
- [main_strmlt-segmentation.yml](.github/workflows/main_strmlt-segmentation.yml) : Workflow Github Actions pour l'application streamlit.

### 📁 [api](api)

- [app.py](api/app.py) : Fichier principal de l'api.
- model.keras (non inclus car trop lourd)
- [test_app.py](api/test_app.py) : Tests pour l'api.
- [requirements.txt](api/requirements.txt) : Dépendances pour l'API.

### 📁 [streamlit](streamlit)

- [app.py](streamlit/app.py) : Fichier principal de l'application.
- [requirements.txt](streamlit/requirements.txt) : Dépendances pour Streamlit.

### 📁 data (Non inclus car fichier trop volumineux)

- Répertoire contenant les données nécessaires pour le projet retrouvables sur [Cityscapes](https://www.cityscapes-dataset.com/dataset-overview/).

### 📄 [Segmentation.ipynb](Segmentation.ipynb) 
- Notebook avec les différentes modélisations.


### 📄 [note_technique.pdf](note_technique.pdf) : 

- Note technique présentant les différentes approches et résultats obtenus.


### 📄 [load_model.py](load_model.py) : 

- Script pour charger le modèle stocké dans Azure.

### 📄 [.gitignore](.gitignore)

- Fichier pour ignorer les fichiers et répertoires spécifiés lors du contrôle de version.

### 📄 [requirements](requirements)

- Dépendances pour lancer les tests unitaires lors du déploiement.

### 📄 [README.md](README.md)

- Le présent fichier, décrivant le projet et sa structure.

---

Merci de consulter ce README pour toute information relative au projet.

---

👩‍💻 **Contributeurs :**
- [Thérèse Vernet](https://www.linkedin.com/in/therese-vernet/)



