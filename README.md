# Projet de Programmation 1

![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)

---

## Création du site d'exercices

---

## Projet réalisé par

### Groupe 34 :

- **Reynier** Theo 22008945 (Groupe C)
- **Hommais** Anthony 22010461 (Groupe C)
- **Fay** Corentin 22013398 (Groupe C)
- **Kechaou** Sonia 21900155 (Groupe C)

---

## Listes des fonctionnalités implémentés

- Utilisation de SQLAlchemy pour définir une base de donnée (voir Procédure)
- **Création** de questions
    - Création d'énoncé
    - Création de réponses
    - Ajout d'étiquettes thématiques
- **Modification** de questions
    - Modification d'un énoncé
    - Changement d'étiquettes
- **Suppresion** de questions
    - Suppression de l'énoncé
    - Suppresion des réponses de la question
- **Editeur**
- **Visualiseur**
- **Liste des questions** créés par l'utilisateur
- **Création** de **comptes utilisateur**
- **Connexion** d'utilisateurs
- **Chaque utilisateur** à ses propres questions et étiquettes
- Possible d'attribuer **plusieurs étiquettes** à une question
- Possibilité de créer de nouvelles étiquettes, de les modifier et de les supprimer
- **Markdown** dans l'éditeur/visualiseur (Showdown)
- **LateX** dans l'éditeur/visualiseur    (MathJax)
- **Code** dans l'éditeur/visualiseur (HighLightJS)
- Possibilité d'indiquer si **une réponse** est juste ou fausse
- Possibilité de mettre du **code,LateX...** dans les réponses
- Possibilité de choisir un certain nombre d'exercices pour **générer une page avec un titre**
- Possibilité dans la liste des questions de **filtrer** avec des **étiquettes**
- Sécurité connexion
    > Empeche un utilisateur d'aller sur certaines pages s'il n'est pas connecté


---

## Listes de ce qui ne fonctionne pas

- Mermaid
- Visualisation des réponses
- Modification d'une réponse

---
## Schéma base de donnée
![Base de donnée](/static/BDD.png)

---
## Procédure

### Créer l'environnement virtuel
```bash
python3 -m virtualenv venv
```

### Activer l'environnement
```bash
venv\bin\activate.bat (Windows)
. venv/bin/activate (linux,macOS)
```

### Installation de Flask 
```bash
pip install flask
```

### Installation SQLAlchemy
```bash
pip install flask-sqlalchemy
```

### Installation Markdown Flask
```bash
pip install Flask-Markdown
```

### Lancer le serveur
```bash
python3 serveur.py
```

---
## Références

- Bouton radio custom : https://www.creativejuiz.fr/blog/tutoriels/personnaliser-aspect-boutons-radio-checkbox-css
- Framework markdown : https://showdownjs.com/
- Framework LateX : https://www.mathjax.org/
- Framework mermaid : https://mermaid.js.org/#/
- Framework code : https://highlightjs.org/