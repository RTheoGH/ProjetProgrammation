# Projet de Programmation

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

### Partie 1 :

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

### Partie 2 :

- **Modification** de l'accueil
    > Acces à un espace pour les enseignants et un autre pour les étudiants
- **Cryptage** des mots de passe
- **Création/Suppression** de comptes étudiants
    > Les enseignants peuvent créer des comptes étudiants manuellement mais peuvent aussi fournir un fichier csv
- Possibilité de **mofidier son mot de passe** pour un utilisateur/étudiant
    > Les enseignants et les étudiants peuvent modifier leur mot de passe dans l'accueil
- **Organisation** des fichiers
    > Création de dossiers pour ranger les fichiers html
- **Fichiers** base/flash.html
    > Le fichier base.html est la base de chaque fichier html, et le fichier flash.html contient le code pour l'affichage des messages flash
- **Responsivité** du site
    > Affichage du site selon la taille de l'écran / affichage pour téléphone
    - Taille d'écran 1024px, 1280px, 1440px, 1680px...
    - Version mobile
- **Affichage** de la liste des QCMs créés
    > Onglet "consulter QCM"
- **Création de QCM** (série de questions)
    > Crée un QCM l'ajoute désormais dans une liste
- Possibilité de **modifier** ou **supprimer** un QCM
- Possibilité **d'afficher** un QCM puis de le **télécharger**
    > En accedant à un QCM, il est possible de le télécharger via le bouton en bas de celui-ci
- Possiblité de **caster** une question/une séquence/QCM
    > Un enseignant choisi s'il souhaite envoyer une question ou une séquence/QCM sur la page de réponse pour les étudiants
- Utilisation de **socket.io** pour faire communiquer deux pages ensemble
    > Socket.io permet à deux pages de communiquer entre elle via des WebSockets (connexion bi-directionnelles)

---

## Listes de ce qui ne fonctionne pas / pas implémenté

- Mermaid
- Questions en direct

---
## Schéma base de donnée
![Base de donnée](/static/image/BDD.png)

---
## Procédure

### Créer l'environnement virtuel
```bash
python -m venv venv
```

### Activer l'environnement
```bash
venv\Scripts\activate.bat (Windows)
. venv/bin/activate (linux,macOS)
```

### Installation des dépendances
```bash
pip install -r requirements.txt
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