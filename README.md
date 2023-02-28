# Projet de Programmation 2

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

| Nom          | Prénom       | Numéro d'étudiant |   Groupe   |
|--------------|--------------|-------------------|------------|
| Reynier      | Théo         | 22008945          | Groupe C   |
| Hommais      | Anthony      | 22010461          | Groupe C   |
| Fay          | Corentin     | 22013398          | Groupe C   |
| Kechaou      | Sonia        | 21900155          | Groupe C   |

---

## Listes des fonctionnalités implémentés

- Utilisation de SQLAlchemy pour définir une base de donnée
    > Voir Schéma,Procédure et fichier bdd.py.
- **Barre de navigation**
    > Barre de navigation disponible sur chaque page, il est important de préciser que les onglets sont disponibles, une fois qu'un utilisateur s'est connecté (voir plus bas).
- **Création** de questions
    - Création d'énoncé
    - Création de réponses
    - Ajout d'étiquettes thématiques
- **Modification** de questions
    - Modification d'un énoncé
    - Modification d'une réponse
    - Changement d'étiquettes
- **Suppresion** de questions
    - Suppression de l'énoncé
    - Suppresion des réponses de la question
- **Editeur**
    > Dans 'Créer Question', partie de gauche.
- **Visualiseur**
    > Dans 'Créer Question', partie de droite.
- **Liste des questions** créés par l'utilisateur
    > Dans 'Consulter Questions'.
- **Création** de **comptes utilisateur**
    > Il faut d'abord créer un compte avant de se connecter.
- **Connexion** d'un utilisateur
- **Deconnexion** d'un utilisateur
- Possiblité d'accéder à **une liste des utilisateurs**
    > L'onglet 'Consulter Utilisateurs' n'est disponible que si le nom de l'utilisateur est 'ADMIN'.
- **Chaque utilisateur** a ses propres questions et étiquettes
- Possibilité d'attribuer **plusieurs étiquettes** à une question
- Possibilité de **créer** de nouvelles **étiquettes**, de les **modifier** et de les **supprimer**
    > Dans l'onglet 'Gérer Etiquette'.
- **Markdown** dans l'éditeur/visualiseur (Showdown)
    > Exemple : ### Titre
- **LateX** dans l'éditeur/visualiseur    (MathJax)
    > Exemple : $x+1=1$
- **Code** dans l'éditeur/visualiseur (HighLightJS)
    > Exemple : ```python
- Possibilité d'indiquer si **une réponse** est juste ou fausse
- Possibilité de mettre du **code,LateX...** dans les réponses
- Possibilité de choisir un certain nombre d'exercices pour **générer une page avec un titre**
    > Dans l'onglet 'Créer un qcm', vous pouvez choisir un titre et choisir des questions, le qcm se genere ensuite avec les énoncés et les réponses.
- Possibilité dans la liste des questions de **filtrer** avec des **étiquettes**
    > Dans la liste de question, cliquez sur une étiquette puis filtrer.
- **Sécurité** connexion
    > Empeche un utilisateur d'aller sur certaines pages s'il n'est pas connecté.

---
## Tâches :
Bloc note de Azouuuu
- modifier l'accueil avec un espace pour les professeurs et un pour les eleves (100%)
- pour le prof faire en sorte qu'il puisse crée un compte ou se connecter (100%)
- pour les eleves seulement se connecter puisque leurs comptes seront crées par le prof (100%)
    - une classe (association maillé), un/des eleves ont un/des professeurs
    - bouton fichier csv
- le mdp des eleves est leur num etudiant (100%)
- crypter les mdp (100%)
- pouvoir modifier les mdp (100%)
- modif la nav barre en fonction si tu es un prof ou un eleve (100%)
- refaire le csv à cause de l'incompatibilité entre les os (100%)
- pouvoir enlever un etudiant de la base (100%)
- bouton deconnexion navbar (100%)
- fichier html avec flash du coup rajouter des include flash (100%)
- modifier etudiant : remplacer id par numeroEtu et enlever numeroEtu (100%)
- affichage ordi (1000,1200,1400,1600...) (10%)
- affichage telephone (75%)
- trier les html (80%)
- commentage (40%)
- bouton imprimer (ouvre onglet avec le qcm) (0%)
- refaire le schéma bdd (0%)
- rapport (1%)
- enfin faire marcher mermaid (0%)

---

## Listes de ce qui ne fonctionne pas / pas implémenté

- Mermaid

---
## Schéma base de donnée
![Base de donnée](/static/image/BDD.png)

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