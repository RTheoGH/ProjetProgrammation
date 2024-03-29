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
- Création d'**ID aléatoire alphanumérique**
    > Génération d'id aléatoire pour les questions etc.
- Fichier **requirements.txt**
    > Fichier pour installer les dépendances
- **Affichage en direct** coté enseignant
- **Affichage en direct** coté étudiant

### Partie 3 :

- Finition de **Question en direct** / **affichage en direct** **(Partie 2)**
- Récupération des **statistiques** d'un étudiant sur une séquence **(Partie 2)**
- Génération de **contrôles**
    > A partir des étiquettes, l'enseignant peut créer des contrôles aléatoires avec un certain nombre de questions par étiquettes sans quelle soit redondante et chaque contrôle est différent
- Possibilité **d'imprimer** un sujet
- Possibilité **d'imprimer** plusieurs contrôles sur un même PDF
- **Deux** possibilités :
    - version **classique** (nom,prénom,numéro)
    - version **anonyme** (numéro d'anonymat)
- **Traitement du langage**:
    - correcteur **orthographique** (**language_tool_python** : voir références)
    - transformation des mots en **minuscule**
    - transformation des mots au **singulier** (**spacy** : voir références)
- Page **d'écriture** d'une question ouverte
    > Coté enseignant, celui-ci peut écrire une question ouverte, celle-ci s'affichera sur cette même page.
- Page de **réponses** d'une question ouverte
    > Coté étudiant, celui-ci peut proposer une réponse à la question ouverte de l'enseignant
- Affichage du **nuage de mots**
    > Quand il le souhaite, l'enseignant peut afficher les résultats sous forme de nuage de mots des réponses fournis par ses étudiants

### Explication Technique :

#### Contrôle aléatoire
Premièrement, la route récupère l'ordre, le minimum et le maximum de questions à mettre dans le QCM, puis vérifie qu'elle ne traite que les étiquettes qui sont demandées dans le formulaire. Elle vérifie ensuite si un ordre d'étiquettes a été appliqué. Si c'est le cas, elle change l'ordre de traitement des étiquettes. Elle continue en récupérant toutes les questions liées aux étiquettes demandées et renvoie une erreur si elle se rend compte que le nombre de questions est insuffisant.

À partir de ce point, elle commence à organiser les données pour créer les QCM. Elle choisit un nombre de questions par étiquette dans la fourchette donnée par l'utilisateur et choisit aléatoirement ce nombre de questions dans la liste de questions récupérées plus tôt pour cette étiquette. Lorsqu'un nouveau set de questions est trouvé, on l'utilise pour créer un nouveau QCM, on trouve un ID non utilisé et on applique l'ordre demandé lors de la création de ce QCM. Pour finir, on ajoute ce QCM dans une liste. On utilise cette liste de QCM dans une fonction externe prenant en entrée une liste de questions et une liste de QCM pour vérifier qu'aucun QCM ne possède ce set de questions (et qu'il n'y a pas de QCM en doublons).

#### Question ouverte
Pour regrouper des termes semblables, on utilise language_tool pour python qui permet dans un premier temps de vérifier si une erreur orthographique est présente dans les termes, puis on retire toute majuscule dans les termes et enfin on met chaque terme au singulier grâce à Spacy.
Ces méthodes permettent de regrouper des mots, termes et phrases, par exemple pour un mot : "Bureau", "buro", "Burau", "bureau", "BUREAU" et "Bureaux" seront tous regroupés par le mot "bureau".

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

### Dictionnaire français pour les mots singuliers/pluriels
(Certain cas nécessite Java : https://www.java.com/fr/)
```bash
python -m spacy download fr_core_news_sm 
```

### Lancer le serveur
```bash
python3 serveur.py
```

Le premier lancement peut être assez long selon la machine utilisée.

---
## Références

- Bouton radio custom : https://www.creativejuiz.fr/blog/tutoriels/personnaliser-aspect-boutons-radio-checkbox-css
- Framework markdown : https://showdownjs.com/
- Framework LateX : https://www.mathjax.org/
- Framework mermaid : https://mermaid.js.org/#/
- Framework code : https://highlightjs.org/
- Language_tool_python : https://pypi.org/project/language-tool-python/
- Spacy : https://spacy.io/
- Chargement : https://codepen.io/WebSonata/pen/bRaONB