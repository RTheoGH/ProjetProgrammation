from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.datastructures import MultiDict, ImmutableMultiDict
from werkzeug.security import generate_password_hash,check_password_hash
import random
import string
import csv
from datetime import datetime
from flask_socketio import SocketIO
import time

app = Flask(__name__)                                         # Création de app, instance de Flask
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'                      # Clé de session (utilisateurs)

from bdd import *                                             # Importation de la base de donnée depuis bdd.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projet.db' # Création du fichier de la base de donnée
db.init_app(app)
socket = SocketIO(app)

# with app.app_context(): 
#     db.drop_all()
#     db.create_all()
# si le "with" n'est pas commenté:
#       si vous rechargez le serveur sans vous deconnecter, une erreur arrive au niveau de l'accueil,
#          utilisez la route /deconnexion pour corriger le probleme

nombreIdQuestion=0               # Variables utilisés pour 
nombreIdCheck=0                  # La génération de réponses
nombreIdQCM=0
checkCodeQcmProf = {}

def createId():                  # Fonction appelée à chaque fois qu'on a besoin de générer un nouvel id
    id=""
    for _ in range(8):
        id+=(random.choice((string.ascii_letters)+("0123456789")))
    return id

@app.route("/")                  # Route principale
def index():                                         # 'page' est la référence de chaque page web actuelle
    title='Accueil'
    if 'nomU' not in session :                       # Accueil si aucun utilisateur n'est connecté
        return render_template("accueil/index.html",title=title,page="Menu") #coloré en rouge dans la barre de navigation
    else:
        if session['role']=='enseignant':            # Accueil si l'utilisateur connecté est un enseignant
            enseignantCO= db.session.query(Utilisateur).filter(Utilisateur.idU==session['idU']).first()
            return render_template("accueil/index.html",title=title,page="Menu",idU=enseignantCO.idU)
        elif session['role']=='etudiant':            #Accueil si l'utilisateur connecté est un etudiant
            etudiantCO = db.session.query(Etudiant).filter(Etudiant.numeroEtu==session['idU']).first()
            return render_template("accueil/index.html",title=title,page="Menu",numeroEtu=etudiantCO.numeroEtu)

@app.route("/espEnseignant")                         # Espace dédié aux enseignants
def espEnseignant():
    title='Espace Enseignant'
    return render_template("accueil/espEnseignant.html",title=title,page="Menu")

@app.route("/espEtudiant")                           # Espace dédié aux etudiants
def espEtudiant():
    title='Espace Etudiant'
    return render_template("accueil/espEtudiant.html",title=title,page="Menu")

@app.route("/creationCompteEnseignant",methods = ['POST', 'GET'])   # Route pour créer un compte utilisateur
def creationCompteEnseignant():
    title='Creation de compte'
    if request.method == 'POST':
        nomUtilisateur = request.form['creationNom']                # generate_password_hash est une methode de
        mdpUtilisateur = request.form['creationMdp']                # werkzeug.security pour crypter les mot de passes
        new_utilisateur = Utilisateur(nomU=nomUtilisateur,passU=generate_password_hash(mdpUtilisateur, method='pbkdf2:sha256', salt_length=16))

        try:
            db.session.add(new_utilisateur)               # Création du nouveau compte
            db.session.commit()
            return redirect(url_for("espEnseignant"))
        except:
            return 'Erreur lors de la création du compte'
    else: 
        return render_template("compte/creationCompteEnseignant.html",title=title,page="Menu")

@app.route("/listeUtilisateurs",methods = ['GET'])        # Cette route est uniquement technique pour pouvoir
def listeUtilisateurs():                                  # visualiser les utilisateurs en aucun cas elle doit
    title='PRIVATE'                                       # etre accessible via une redirection ou autre.
    if 'nomU' not in session or session['nomU']!='ADMIN': 
        flash("Vous n'avez pas les droits pour accéder à cette page")  # Si vous souhaitez néanmoins accéder à la
        return redirect(url_for('index'))                              # page, créez un compte 'ADMIN' puis
    utilisateurs = db.session.query(Utilisateur).all()                 # connectez vous avec.
    return render_template("liste/lUtilisateurs.html",lUtilisateurs=utilisateurs,title=title,page='ListeUtilisateurs')

@app.route("/listeEtudiants",methods=['POST','GET'])
def listeEtudiants():
    title='Etudiants'
    if 'nomU' not in session:                                           # Sécurité pour éviter d'aller sur une page
        flash("Connectez vous ou créer un compte pour accéder à cette page") #sans se connecter
        return redirect(url_for('index'))
    if request.method == 'POST':
        if 'fichierEtu' in request.files:
            fichierCsv = request.files['fichierEtu']                    # récupération du fichier depuis l'html
            if fichierCsv.filename != '':
                contenuCsv = []                                               # Contenu du fichier sous forme de liste de listes
                decoded_file = fichierCsv.read().decode('iso-8859-1')         # Decodeur (iso equivalent de utf-8)
                reader = csv.reader(decoded_file.splitlines(), delimiter=';') # Début de la lecture du fichier
                next(reader)                                                  # on ignore la ligne avec les titres des colonnes
                for ligne in reader:
                    contenuCsv.append(ligne)

                for eleve in contenuCsv:                                    # Ajout des elèves dans la base de donnée
                    new_etudiant=Etudiant(numeroEtu=int(eleve[2]),nomEtu=eleve[0],prenomEtu=eleve[1],\
                        mdpEtu=generate_password_hash(eleve[2],method='pbkdf2:sha256',salt_length=16))
                    try:
                        db.session.add(new_etudiant)
                        db.session.add(Classe(idCE=new_etudiant.numeroEtu,idCU=session['idU']))
                        db.session.commit()
                    except Exception as e:
                        return str(e)
            return redirect(url_for("listeEtudiants"))
        else:
            nomEtudiant=request.form['nomEtu']                              # Ajout d'un elève dans la base de donnée
            prenomEtudiant=request.form['prenomEtu']                        # manuellement
            numeroEtudiant=request.form['numeroEtu']
            new_etudiant=Etudiant(numeroEtu=numeroEtudiant,nomEtu=nomEtudiant,prenomEtu=prenomEtudiant,\
                mdpEtu=generate_password_hash(numeroEtudiant, method='pbkdf2:sha256', salt_length=16))

            try:
                db.session.add(new_etudiant)               
                db.session.commit()                        
                db.session.add(Classe(idCE=new_etudiant.numeroEtu,idCU=session['idU']))
                db.session.commit()
                return redirect(url_for("listeEtudiants"))
            except Exception as e:
                return str(e)
    else:
        etudiants = db.session.query(Etudiant).filter(Etudiant.numeroEtu==Classe.idCE,Classe.idCU==session['idU']).all()
        return render_template("liste/lEtudiants.html",lEtudiants=etudiants,title=title,page='ListeEtudiants')

@app.route("/retirerEtu/<int:id>")                    # Route pour retirer un étudiant
def retirerEtu(id):
    if 'nomU' not in session:                           # Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    etudiantMoins = Etudiant.query.get_or_404(id)                          # Récupération étudiant
    classeMoins = db.session.query(Classe).filter(Classe.idCE==id).first() # Récupération classe
    
    try:
        db.session.delete(classeMoins)                  # Suppression classe
        db.session.delete(etudiantMoins)                # Suppression etudiant
        db.session.commit()                             # Envoi des modifications à la base de données
        return redirect(url_for('listeEtudiants'))      # Redirection vers la liste d'étudiants
    except:
        return 'Erreur lors de la suppression'

@app.route("/connexionEnseignant",methods=['POST','GET'])           # Route pour se connecter
def connexionEnseignant():
    title='Connexion Enseignant'
    if request.method == 'POST':
        testLogin = db.session.query(Utilisateur).filter(Utilisateur.nomU == request.form['nomU']).first()
        if testLogin is None:
            flash('Nom invalide')                                        # Il faut d'abord crée un compte
            return redirect(url_for('connexionEnseignant'))              # check_password_hash est une methode de
        if check_password_hash(testLogin.passU,request.form['passU']):   # werkzeug.security pour verifier qu'un mot de passe
            session['nomU'] = request.form['nomU']                       # correspond avec le cryptage
            session['idU'] = testLogin.idU
            session['role'] = "enseignant"
        else:
            flash('Mot de passe invalide')             
            return redirect(url_for('connexionEnseignant'))  
        return redirect(url_for("index"))              
    else:                       
        return render_template("compte/connexionEnseignant.html",title=title,page="Menu")

@app.route("/connexionEtudiant",methods=['POST','GET'])           # Route pour se connecter
def connexionEtudiant():
    title='Connexion Etudiant'
    if request.method == 'POST':
        testLogin = db.session.query(Etudiant).filter(Etudiant.nomEtu == request.form['nomU']).first()
        if testLogin is None:
            flash('Nom invalide')             # Il faut d'abord crée un compte
            return redirect(url_for('connexionEtudiant'))  
        if check_password_hash(testLogin.mdpEtu,request.form['passU']): # Vérifie que le mdp correspond
            print("mot de passe correspondant")     
            session['nomU'] = request.form['nomU']            
            session['idU'] = testLogin.numeroEtu
            session['preU'] = testLogin.prenomEtu
            session['role'] = "etudiant"
        else:
            flash('Mot de passe invalide')             
            return redirect(url_for('connexionEtudiant'))  
        return redirect(url_for("index"))              
    else:                       
        return render_template("compte/connexionEtudiant.html",title=title,page="Menu")

@app.route("/modifMdp/<int:id>",methods=['POST','GET'])          # Route pour modifier son mot de passe
def modifMdp(id):
    title='Modification Mot de passe'
    if 'nomU' not in session :                                          # Sécurité pour éviter d'aller sur une page
        flash("Connectez vous ou créer un compte pour accéder à cette page") # sans se connecter
        return redirect(url_for('index'))
    if request.method == 'POST':
        mdpActuel=request.form['mdpActu']            # Mot de passe actuel
        newMdp=request.form['nMdp']                  # Nouveau mot de passe
        if session['role']=='etudiant':                                # Pour les étudiants
            mdpAModif = Etudiant.query.get_or_404(id)
            print("numero a modifier:",mdpAModif)
            if check_password_hash(mdpAModif.mdpEtu,mdpActuel):        # Verifie la correspondance mdp entré/mdp actuel
                mdpAModif.mdpEtu = generate_password_hash(newMdp, method='pbkdf2:sha256', salt_length=16) #Attribue le nouveau mdp
                # print("j'attribue le nouveau mot de passe ! :",newMdp)
                db.session.commit()
                flash("Mot de passe modifié avec succès")
                return redirect(url_for("index"))
            else:
                flash("Mot de passe actuel incorrect")
                # print("tu as entré :",mdpActuel)
                return redirect(url_for("index"))
        elif session['role']=='enseignant':                            # Pour les enseignants
            mdpAModif = Utilisateur.query.get_or_404(id)
            if check_password_hash(mdpAModif.passU,mdpActuel):
                print("hello ?")                                       # Verifie la correspondance mdp entré/mdp actuel
                mdpAModif.passU = generate_password_hash(newMdp,method='pbkdf2:sha256',salt_length=16)
                db.session.commit()
                flash("Mot de passe modifié avec succès")
                return redirect(url_for("index"))
            else:
                flash("Mot de passe actuel incorect")
                return redirect(url_for("index"))
        else:
            return "Erreur : aucun role ne correspond"
    else:
        if session['role']=='etudiant':
            etudiantCO = db.session.query(Etudiant).filter(Etudiant.numeroEtu==session['idU']).first()
            return render_template("compte/modifMdp.html",title=title,page="Menu",idMAModif=etudiantCO.numeroEtu)
        elif session['role']=='enseignant':
            enseignantCO = db.session.query(Utilisateur).filter(Utilisateur.idU==session['idU']).first()
            return render_template("compte/modifMdp.html",title=title,page="Menu",idMAModif=enseignantCO.idU)

@app.route("/deconnexion")                        # Route de deconnexion
def deconnexion():                                # Retire l'utilisateur de la session
    session.pop('nomU',None)
    return redirect(url_for("index"))

@app.route("/ajout",methods = ['POST', 'GET'])    # Route pour ajouter une question
def ajout():
    title='Ajout'
    if 'nomU' not in session :                                          # Sécurité pour éviter d'aller sur une page
        flash("Connectez vous ou créer un compte pour accéder à cette page") #sans se connecter
        return redirect(url_for('index'))
    if session['role'] != 'enseignant' :                      # Si vous n'êtes pas prof
        flash("Vous n'avez pas les droits nécéssaires")           
        return redirect(url_for('index'))

    if request.method == 'POST':                  # Recupere question du formulaire
        question = request.form['question']       # Création nouvelle question avec enoncé correspondant  
        
        idQuest = createId()
        while idQuest in db.session.query(Question.idQ):
            idQuest = createId()

        new_question = Question(idQ=idQuest,enonce=question,idU=session['idU'])
        
        recupForm = request.form.getlist("reponse")     # On récupère la liste des questions
        if recupForm == []:
            # rep_num1 = request.form["rep_num1"]
            # rep_num2 = request.form["rep_num2"]
            # rep_num = float(rep_num1) + float(float(rep_num2)*0.01)
            rep_num = request.form["Rep_num"]
            print("rep num = ", rep_num)
                

        #try:
        db.session.add(new_question)                # Ajout question -> base de donnée            
        db.session.commit()                         # Envoie des changements
        idQuestion = db.session.query(Question.idQ).filter(Question.enonce == question).first()
        if recupForm == []:
            db.session.add(Reponse(reponse=rep_num,correction = 1,estNumerique = True,idQ=idQuestion[0]))
            
        listeOn = []                              
        for key,value in request.form.items():      # Pour chaque item du formulaire
            if value == 'on':
                listeOn.append(int(key))            # Attribut d'id pour la question
        
        for rep in recupForm:
            reponseAjouter = 0
            if (recupForm.index(rep)+1) in listeOn: # On ajoute réponse juste
                reponseAjouter = Reponse(reponse= rep,correction = 1,idQ =idQuestion[0])
                db.session.add(reponseAjouter)
            else:                                   # On ajoute réponse fausse
                reponseAjouter = Reponse(reponse= rep,correction = 0,idQ =idQuestion[0])
                db.session.add(reponseAjouter)       
        db.session.commit()
        

        print("idquestion de 0 = ",idQuestion[0]," id question en tout = ",idQuestion)
        print(db.session.query(Reponse.reponse).filter(Reponse.idQ == idQuestion[0]).all())#test
        selected_tags = request.form.getlist('tag') # On récupère la liste des étiquettes
        for tag_id in selected_tags:
            new_assos = Associe(RidE=tag_id,RidQ=new_question.idQ) # On crée l'association entre question
            db.session.add(new_assos)                              # et étiquette
            db.session.commit()                     # Envoie des changements
        print("reponse.exe = ",db.session.query(Reponse.reponse).filter(Reponse.idQ==idQuestion[0]).all())
        return redirect(url_for('lQuestion'))       # Redirection vers la liste des questions
        # except:
        #    return 'Erreur création de la question'
    else:
        return render_template("question/ajoutQuestion.html",title=title,page="Créer")

@app.route("/creationEtiquettes",methods=['GET','POST']) # Route pour créer une étiquette
def creationEtiquettes():
    title='Etiquette'
    if 'nomU' not in session:                            # Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    if request.method == 'POST':
        nom = request.form['nom']
        new_etiquette = Etiquette(nom=nom,idU=session['idU'])

        try :
            db.session.add(new_etiquette)                # Ajout de l'étiquette
            db.session.commit()
            print(Etiquette.query.all(),new_etiquette.nom,new_etiquette.idE)
            return redirect(url_for('creationEtiquettes'))
        except:
            return 'Erreur : route /creationEtiquettes'
    else :
        ToutEtiq = db.session.query(Etiquette).filter(Etiquette.idU==session['idU']).all()
        return render_template("question/creationEtiquettes.html",title=title,page="Etiquettes",etiqs=ToutEtiq)

@app.route("/suppEtiquettes",methods=['GET','POST'])     # Route pour supprimer une étiquette
def suppEtiquettes():
    title='Etiquette'
    if 'nomU' not in session:                            # Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    if request.method == 'POST':
        nom = request.form['nom']
        
        try :                                            # On associe avec l'étiquette puis on sélectionne l'étiquette en question
            test = db.session.query(Associe).join(Etiquette,Associe.RidE == Etiquette.idE).filter(Etiquette.nom == nom,Etiquette.idU==session['idU']).all()
            etiq = db.session.query(Etiquette).filter(Etiquette.nom==nom,Etiquette.idU==session['idU']).first()
            for associe in test:
                db.session.delete(associe)
                db.session.commit()
            else:
                print("Etiquette not found")             # Si on ne trouve pas l'étiquette
            db.session.delete(etiq)
            db.session.commit()
            return redirect(url_for('creationEtiquettes'))
        except:
            return 'Erreur : route /suppEtiquettes'
    else :
        return render_template("question/creationEtiquettes.html",title=title,etiqs=ToutEtiq)

@app.route("/modifEtiquettes",methods=['GET','POST'])     # Route pour modifier une étiquette
def modifEtiquettes():
    title='Etiquette'
    if 'nomU' not in session:                             # Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    if request.method == 'POST':
        nom = request.form['nom']
        etiqIde = request.form['etiqAmodif']              # Recupere l'étiquette à modifier

        try :                                             # Sélectionne l'étiquette en question
            etiqAmodif = db.session.query(Etiquette).filter(Etiquette.idE==etiqIde)
            etiqAmodif.update({"nom" : nom })             # Change le nom
            db.session.commit()
            return redirect(url_for('creationEtiquettes'))
        except:
            return 'Erreur : route /modifEtiquettes'
    else :
        return render_template("question/creationEtiquettes.html",title=title,etiqs=ToutEtiq)

@app.route("/creerQuestion",methods=['GET','POST'])       # Route pour afficher les étiquettes sur ajoutQuestion
def creerQ():
    title='Ajout'
    if 'nomU' not in session:                             # Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    etiquettes = db.session.query(Etiquette).filter(Etiquette.idU==session['idU']).all()
    return render_template('question/ajoutQuestion.html',title=title,etiquettes=etiquettes, page="Créer")

@app.route("/plusDeReponse",methods = ['GET'])          # Route qui ajoute une réponse sur ajoutQuestion
def plusDeReponse():
    global nombreIdQuestion,nombreIdCheck               # Déclaration variables globales nombreIdQuestion, nombreIdCheck
    nombreIdQuestion+=1                                 # Incrémentation de nombreIdQuestion et nombreIdCheck
    nombreIdCheck+=1                                    # de 1 (pour avoir des id différent pour chaque objet)
    return render_template('partials/nouvelleReponse.html',IdBouton=nombreIdQuestion,IdCheck=nombreIdCheck)
    # Rendu template 'partials/nouvelleReponse.html' et passage des paramètres IdBouton et IdCheck

@app.route("/supprimer_bouton", methods=['DELETE'])     # Route qui supprime une réponse sur ajoutQuestion
def supprimer_bouton():
    id = request.json['id']
    return 'SUCCES'

@app.route("/lQuestion",methods = ['GET'])              # Route vers la liste de questions de l'utilisateur
def lQuestion():
    title='Bibliothèque'
    if 'nomU' not in session:                           # Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))               # Sélection des questions et étiquettes
    etiquettes = db.session.query(Etiquette).filter(Etiquette.idU==session['idU']).all()
    questions = db.session.query(Question).filter(Question.idU==session['idU']).all()
    return render_template("liste/lQuestion.html",title=title,etiquettes=etiquettes,lquestion=questions,page="ListeQuestions")

@app.route("/filtre",methods = ['GET','POST'])          # Route de filtrage des questions de l'utilisateur
def filtre():
    title='Bibliothèque'
    etiquettes = db.session.query(Etiquette).filter(Etiquette.idU==session['idU']).all()
    tags = request.form['tag']
    if request.method == 'POST':                        # Affiche les questions avec les tags sélectionnés
        questionAffiche = db.session.query(Question).join(Associe, Associe.RidQ == Question.idQ)\
            .join(Etiquette, Etiquette.idE == Associe.RidE).filter(Etiquette.idE == tags,Etiquette.idU==session['idU']).all()
        return render_template("liste/lQuestion.html",title=title,etiquettes=etiquettes, lquestion=questionAffiche, page="ListeQuestions")

@app.route("/modifier/<string:id>",methods=['POST','GET']) # Route pour modifier une question de l'utilisateur
def modifier(id):
    title='Modification Question'
    if 'nomU' not in session:                           # Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    selected_tags = request.form.getlist('tag')
    questionModif = Question.query.get_or_404(id)       # Recup question avec id correspondant, erreur sinon
    reponseModif = Reponse.query.filter(Reponse.idQ==questionModif.idQ).all() #Recup les reponses de la question
    ToutAssoc = db.session.query(Associe).filter(Associe.RidQ==questionModif.idQ).all()
    
    if request.method == 'POST':
        questionModif.enonce = request.form['question'] # Modification de l'enoncé de la question
        for r in reponseModif:                          # Pour chaque reponse, modifie tout
            r.reponse = request.form['R'+str(r.idR)]
        
        try:
            db.session.query(Associe).filter(Associe.RidQ == id).delete()
            db.session.commit()                         # Envoi des modifications à la base de données
            for tag_id in selected_tags:
                new_assos = Associe(RidE=tag_id,RidQ=questionModif.idQ)
                db.session.add(new_assos)
                db.session.commit()  
            return redirect(url_for('lQuestion'))       # Redirection vers la page de liste des questions
        except:
            return 'Erreur de modification'             # Renvoi message erreur en cas d'échec de la modification
    else:
        etiquettes = db.session.query(Etiquette).filter(Etiquette.idU==session['idU']).all()
        return render_template("question/modifQuestion.html",title=title,enonce=questionModif.enonce,\
            idQ=questionModif.idQ,reponses=reponseModif,etiquettes=etiquettes,page="ListeQuestions")

@app.route("/supprimer/<string:id>")                    # Route pour supprimer une question de l'utilisateur
def supprimer(id):
    if 'nomU' not in session:                           # Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    questionSupp = Question.query.get_or_404(id)        # Récupération question correspondant id, sinon erreur
    toutAssocie = db.session.query(Associe).all()    
    reponseSupp = db.session.query(Reponse.idR).filter(Reponse.idQ==id).all()
    qcmAssocie = db.session.query(Contient).filter(Contient.RidQ==id).all()

    try:
        for key in reponseSupp:                         # Supprime toutes les réponses
            Asupp = Reponse.query.get_or_404(key)
            db.session.delete(Asupp)
        for assoc in toutAssocie :                      # Supprime toutes les associations
            if(assoc.RidQ==id):
                db.session.delete(assoc)
                db.session.commit()
        for key in qcmAssocie:
            db.session.delete(key)
        db.session.delete(questionSupp)                 # Suppression question de la base de données
        db.session.commit()                             # Envoi des modifications à la base de données
        return redirect(url_for('lQuestion'))           # Redirection vers la page de liste des questions
    except:
        return 'Erreur lors de la suppression de la question'
        #Renvoi message d'erreur si échec de la suppression de la question

@app.route("/listeQCM",methods = ['GET','POST'])      # Route pour la liste des qcm et créer de nouveaux QCM
def listeQCM():
    title='Vos QCM'
    if 'nomU' not in session:                   # Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    
    if request.method == 'POST':              # Création de QCM
        idQcm = createId()                    # Génération d'un id
        while idQcm in db.session.query(QCM.idQCM): #Id unique
                idQcm = createId()
        nomQcm = request.form['nomQcm']       # Récupération du nom du QCM
        new_QCM = QCM(idQCM=idQcm,Nom=nomQcm,idU=session['idU']) # Création du QCM

        try : 
            db.session.add(new_QCM)           # Ajout à la base de donnée
            db.session.commit()
        except : 
            return 'Erreur dans la création du QCM'
        for key, value in request.form.items():                # Association du QCM à ses Questions
            if value == 'on':                                  # key=idQuestion ; value=valeur du commutateur
                new_contient = Contient(RidQCM=idQcm,RidQ=key)

                try :
                    db.session.add(new_contient)      # Ajout des relations
                    db.session.commit()
                except :
                    return "Erreur de création du lien 'contient' entre Qcm et Question"
        return redirect("/listeQCM")                  # Retour vers la liste des QCM
    else:
        etiquettes = db.session.query(Etiquette).filter(Etiquette.idU==session['idU']).all()
        listeQCM = db.session.query(QCM).filter(QCM.idU==session['idU']).all()         # Affichage de tous les QCM
        LQ = db.session.query(Question).filter(Question.idU==session['idU']).all()
        return render_template("liste/lQCM.html",title=title,listeQCM=listeQCM,ListesQuestions=LQ,page="ListeQCM",etiquettes=etiquettes)

def is_same_qcm(questions_qcm, previous_qcms):
    """
    Prend une liste de questions et une liste de qcm en paramètres, et vérifie si l'un des qcm possède
    déjà exactement les questions données, rend True si l'un des qcm les possèdent False sinon
    """
    if not questions_qcm:
        return True
    if previous_qcms:
        for qcm in previous_qcms:
            listeIdQuestions = db.session.query(Contient.RidQ).filter(Contient.RidQCM==qcm.idQCM).all()
            nbQuest = len(listeIdQuestions)
            for IdQuestion in listeIdQuestions:
                quest_diff = 0
                for question in questions_qcm:
                    if question.idQ != IdQuestion:
                        quest_diff += 1
                if quest_diff == nbQuest:
                    return False            
        return True
    else :
        return False

@app.route('/createRandom', methods=['GET', 'POST'])
def create_qcm():
    # Vérifier si l'utilisateur est connecté
    if 'nomU' not in session:
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))

    # Si la méthode est POST, l'utilisateur a soumis un formulaire
    if request.method == 'POST':
        # Récupérer les données du formulaire
        num_qcm = int(request.form['num_qcm'])                      # nombre de QCM à créer
        nom_qcm = request.form['nom_qcm']                           # nom du QCM
        etiquettes_id_form = request.form.getlist('etiquette_id[]') # étiquettes existantes
        etiquettes_ordre = {}                                       #ordres fournis
        nb_questions_min = {}
        nb_questions_max = {}
        nb_Question_total_form = int(request.form['nb_quest'])

        for etiquette_id in etiquettes_id_form:
            etiquettes_ordre[etiquette_id] = int(request.form['etiquettes_ordre[{}]'.format(etiquette_id)])
            nb_questions_min[etiquette_id] = int(request.form['nb_questions_min[{}]'.format(etiquette_id)])
            nb_questions_max[etiquette_id] = int(request.form['nb_questions_max[{}]'.format(etiquette_id)])
            if nb_questions_min[etiquette_id]>nb_questions_max[etiquette_id]:
                nb_questions_min[etiquette_id],nb_questions_max[etiquette_id]=nb_questions_max[etiquette_id],nb_questions_min[etiquette_id]

        for key, etiquette_id in enumerate(etiquettes_id_form):
        #for etiquette_id in etiquettes_id_form:
            if nb_questions_max[etiquette_id]==0:
                etiquettes_id_form.pop(key)

        qcms_crees = []                                         # Liste pour stocker les QCMs créés
        questions = {}                                          # Liste pour stocker les Questions des étiquettes
        toutes_les_valeurs_sont_zero = True
        for valeur in etiquettes_ordre.values():
            if valeur != 0:
                toutes_les_valeurs_sont_zero = False
                break

        if toutes_les_valeurs_sont_zero == True:
            etiquettes_id = etiquettes_id_form
        else :
            etiquettes_id_form_triees = []
            for valeur in etiquettes_ordre.values():
                for cle in etiquettes_ordre.keys():
                    if etiquettes_ordre[cle] == valeur:
                        if cle in etiquettes_id_form:
                            etiquettes_id_form_triees.append(cle)
            liste_sans_doublon = []
            for etiquette_id_doublons in etiquettes_id_form_triees:
                if etiquette_id_doublons not in liste_sans_doublon:
                    liste_sans_doublon.append(etiquette_id_doublons)

            etiquettes_id = liste_sans_doublon

        # Trouver toutes les questions avec l'étiquette spécifiée dans la base de données
        for etiquette_id in etiquettes_id:
            questions[etiquette_id] = Question.query.join(Associe).filter(Associe.RidE == etiquette_id).all()
            etiq = db.session.query(Etiquette.nom).filter(Etiquette.idE==etiquette_id,Etiquette.idU==session['idU']).first()
            # Vérifier si des questions ont été trouvées pour l'étiquette spécifiée
            if not questions[etiquette_id]:
                flash(f"Aucune question trouvée pour l'étiquette {etiq.nom}")
                return redirect(url_for('lQuestion'))

            if len(questions[etiquette_id]) < nb_questions_min[etiquette_id]:
                flash(f"Pas assez de question trouvée pour l'étiquette {etiq.nom}")
                return redirect(url_for('lQuestion'))

        # Créer num_qcm QCMs avec des questions aléatoires sélectionnées à partir de la liste de questions trouvées
        for i in range(num_qcm):
            nb_Question_total = nb_Question_total_form
            selected_questions = []   # Liste pour stocker les questions sélectionnées pour le QCM
            selected_question_ids = set()

            # Définir la limite de temps en secondes
            time_limit = 5

            # Mesurer le temps de début
            start_time = time.time()

            questions_subset = []

            # Sélectionner un nombre aléatoire de questions entre la fourchette spécifiée pour chaque étiquette
            for etiquette_id in etiquettes_id:
                if nb_Question_total == 0:
                    break
                before = []
                if etiquette_id == etiquettes_id[len(etiquettes_id)-1]:
                    nb_questions_subset = nb_Question_total

                if nb_Question_total >= nb_questions_max[etiquette_id]:
                    nb_questions_subset = random.randint(nb_questions_min[etiquette_id], nb_questions_max[etiquette_id])
                    nb_Question_total -= nb_questions_subset
                else :
                    nb_questions_subset = nb_Question_total
                    nb_Question_total = 0
                while nb_questions_subset > len(before):
                    question = random.choice(questions[etiquette_id])
                    if question not in questions_subset:
                        before.append(question)
                        questions_subset.append(question)

            while is_same_qcm(selected_questions, qcms_crees):
                # Vérifier si le temps limite est dépassé
                if time.time() - start_time > time_limit:
                    etiq = db.session.query(Etiquette.nom).filter(Etiquette.idE==etiquette_id,Etiquette.idU==session['idU']).first()
                    flash(f"Veuillez augmenter le nombre de questions possédant l'étiquette {etiq.nom}")
                    return redirect(url_for('lQuestion'))
                
                for question in questions_subset:
                    selected_questions.append(question)
                    selected_question_ids.add(question.idQ)

            # Générer un ID unique pour le QCM
            qcm_id = createId()
            while db.session.query(QCM).filter_by(idQCM=qcm_id).first() is not None:
                # Si l'ID existe déjà dans la base de données, on en génère un nouveau
                qcm_id = createId()


            #Créer un nouveau QCM
            new_qcm = QCM(idQCM=qcm_id, Nom=nom_qcm, idU=session['idU'])
            db.session.add(new_qcm)

            Position = 0
            # Ajouter les questions sélectionnées au QCM
            for question in selected_questions:
                new_contient = Contient(RidQCM=qcm_id, RidQ=question.idQ, Position=Position)
                db.session.add(new_contient)
                Position +=1

            # Ajouter le nouveau QCM à la liste des QCMs créés
            qcms_crees.append(new_qcm)

        # Enregistrer les modifications dans la base de données
        db.session.commit()

        # Afficher un message de confirmation et rediriger vers la liste des QCMs
        flash(f"{num_qcm} QCM(s) ont été créé(s) avec succès!", 'success')
        return redirect(url_for('listeQCM'))
    else:
        flash(f"Vos QCM(s) n'ont pas pu être créé(s)... ")
        return redirect(url_for('listeQCM'))

@app.route("/download-delete",methods=['POST'])
def dl():
    # Vérifier si l'utilisateur est connecté
    if 'nomU' not in session:
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    nom = request.form['nom']
    delete = QCM.query.filter(QCM.idU == session['idU'],QCM.Nom==nom).all()
    num_del = len(delete)
    ##################### Partie Download #####################

    data = []
    data.append(nom)
    for Qcm in delete:
        data_qcm = []
        questions = Question.query.join(Contient, Contient.RidQCM == Qcm.idQCM).filter(Question.idU == session['idU'],Question.idQ==Contient.RidQ,).all()
        for question in questions:
            data_indice = []
            data_indice.append(question.enonce) # énoncé de la question
            reponses = Reponse.query.filter(Question.idU == session['idU'],Reponse.idQ==question.idQ).all()
            reponses_reponse = []
            for reponse in reponses: #Liste des énoncé des réponses
                reponses_reponse.append(reponse.reponse) 
            data_indice.append(reponses_reponse)
            print('data_indice ',data_indice)
            data_qcm.append(data_indice)
        print('data_qcm',data_qcm)
        data.append(data_qcm)
    print("data",data)

    ##################### Fin Download #####################
    # print(delete,"a delete")
    # for Qcm in delete:
    #     print(Qcm)
    #     db.session.query(QCM).filter(QCM.idU == session['idU'],QCM.idQCM==Qcm.idQCM).delete()
    # db.session.commit()
    # print("sortie")
    # if num_del > 0:
    #     flash(f"{num_del} QCM(s) ont été supprimée(s) avec succès!", 'success')
    # else:
    #     flash(f"Aucun QCM trouvé avec ce nom.", 'danger')
    return data

@app.route("/afficheQCM/<string:id>")  # Affichage des questions du Qcm avec leurs réponses
def afficheQCM(id):                    # Remarque : le [0] sert à isoler la chaine de char, puisque la requête renvoie un objet 
    nomQcm = db.session.query(QCM.Nom).filter(QCM.idQCM==id).first()[0]   
    title = nomQcm 
    listeIdQuestions = db.session.query(Contient.RidQ).filter(Contient.RidQCM==id).order_by(Contient.Position).all() # Liste des idQuestions cochées
    checked_questions = []                            # Liste des questions du QCM (objets Question entiers)
    checked_reponses = []                             # Leurs reponses respectives (liste de listes)
    for idQuestion in listeIdQuestions:               # Pour chaque idQuestion, on récupère
        idQuestion = idQuestion[0]
        objetQuestion = db.session.query(Question).filter(Question.idQ==idQuestion).first()
        checked_questions.append(objetQuestion)       # L'objet Question entier
        listeReponse = db.session.query(Reponse).filter(Reponse.idQ==idQuestion).all()
        if (listeReponse[0].estNumerique):
            checked_reponses.append([])
        else:
            checked_reponses.append(listeReponse)     # Et les réponses correspondantes à cette question
    return render_template("qcm/affichage.html",title=title,nomQcm=nomQcm,listeQuestions=checked_questions,\
        listeReponses=checked_reponses,len=len(checked_questions),page="ListeQCM")

@app.route("/entrerCodeEtu",methods =["POST","GET"])
def entrerCodeEtu():
    title='Repondez aux questions'
    if 'nomU' not in session:                   # Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    
    if request.method == "POST":
        code = request.form["code"]
        existe = False
        for key in checkCodeQcmProf.values():
            if code == key:
                existe = True
        if (existe):
            print("le code existe")
            return render_template("wooclap/repondreQCM.html",page="RepondreQCM",title=title,code=code)
        else:
            flash(f"Le code entré n'existe pas!")
            return render_template("wooclap/entrerCodeEtu.html",page="RepondreQCM",title=title)
    else:
        return render_template("wooclap/entrerCodeEtu.html",page="RepondreQCM",title=title)

@app.route("/envoyerEnonce",methods = ["POST","GET"])
def caster():
    title='Envoyer un énoncé'
    if 'nomU' not in session:                   # Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    if request.method == "POST":
        idElementCaste = request.form['radio']
        reponses=[]
        questions=[]
        if 'question' in request.form:
            questions = db.session.query(Question).filter(Question.idQ==idElementCaste).all()
            listeReponse = db.session.query(Reponse).filter(Reponse.idQ==idElementCaste).all()
            if (listeReponse[0].estNumerique):
                reponses.append([])
            else:
                reponses.append(listeReponse)
            typeElement = "question"
        else:
            idQuestions = db.session.query(Contient.RidQ).filter(Contient.RidQCM==idElementCaste).all()
            for quest in idQuestions:                
                objetsQuestion = db.session.query(Question).filter(Question.idQ==quest[0]).first()
                questions.append(objetsQuestion)
                listeReponse = db.session.query(Reponse).filter(Reponse.idQ==quest[0]).all()
                if (listeReponse[0].estNumerique):
                    reponses.append([])
                else:
                    reponses.append(listeReponse)    
            typeElement = "sequence"
        return render_template('wooclap/AttenteConnexionEtudiant.html',title=title,idElement=idElementCaste,listeQuestions=questions,listeReponses=reponses,typeElement=typeElement,page = "EnvoyerEnonce")
    else:
        listeQuestions = db.session.query(Question).filter(Question.idU==session['idU']).all()
        listeQCM = db.session.query(QCM).filter(QCM.idU==session['idU']).all()
        return render_template("wooclap/envoyerEnonce.html",title=title,listeQCM=listeQCM,listeQuestions=listeQuestions,page = "EnvoyerEnonce")
@app.route("/lancerCaste",methods = ["POST","GET"])
def lancerCaste():
    title = 'Envoyer un énoncé'
    if 'nomU' not in session:                   # Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    if request.method == "POST":
        donneesRecup = request.form.getlist('ARecup')
        idElementCaste = donneesRecup[0]
        questions = donneesRecup[1]
        reponses = donneesRecup[2]
        print("donne 3 = ",donneesRecup[3])

        typeElement = donneesRecup[3]
        return render_template('wooclap/casterEnonce.html',title=title,idElement=idElementCaste,listeQuestions=questions,listeReponses=reponses,typeElement=typeElement,page = "EnvoyerEnonce")
    return render_template("/index.html")

##################### Partie Socket #####################

@socket.on('connect')
def test_disconnect():
    print('Client connected') 
@socket.on('disconnect')
def test_disconnect():
    idProf = session['idU']
    if idProf in checkCodeQcmProf.keys():
        socket.emit('profDeco', checkCodeQcmProf[idProf])
        checkCodeQcmProf.pop(idProf)
    print("Client disconnect ", checkCodeQcmProf)



# Socket réception des données envoyés depuis casterEnonce.html
@socket.on('oneByOne')
def oneByOne(q,questions,reponses):
    idClient = request.sid
    questionCastee = str(db.session.query(Question.enonce).filter(Question.idQ==questions[q]).all())
    idReponsesAssociees = reponses[q].split(',')
    reponsesAssociees = []
    if idReponsesAssociees != []:
        for id in idReponsesAssociees:
            reponsesAssociees.append(str(db.session.query(Reponse.reponse).filter(Reponse.idR==id).all()))
    socket.emit('emitOneByOne',(questionCastee,reponsesAssociees),room=idClient)

# Socket réception du numéro de la question actuelle
@socket.on('setQuestion')
def setQuestion(data):
    print(data)
    socket.emit('afficheQuestion',data) # Renvoie le numéro de la question à afficher

# Socket réception des reponses des éléves et les mettres dans la bdd
@socket.on('reponseE')
def reponseE(enonce,reponse_choix,reponse_num):
#         idE = session['idU']
#     add = ReponseQCM(numeroEtu=idE,idQCM=,RidQ=,date=str(datetime.now()),estNumerique=,Value=)
#     db.session.add(add)
#     db.session.commit()
    print("enonce = ",enonce," reponse choix = ",reponse_choix," reponse num = ",reponse_num)

@socket.on('recupDataForRep')
def recupDataForRep(questionCastee, reponsesAssociees,codeQcm):
    print("recupdataforrep liste = ",checkCodeQcmProf )
    idProf = session['idU']
    socket.emit('afficheQuestion',(questionCastee, reponsesAssociees,codeQcm))

@socket.on('reponseEtuChoixmultiple')
def reponseEtuChoixmultiple(reponse_choix,ReponseChoixJS):
    print("rezponsechoix multiple = ", checkCodeQcmProf)
    socket.emit("retourReponseEtudiant",(reponse_choix,ReponseChoixJS))
@socket.on('testQP')
def testQP():
    print("sucess !!!!")
@socket.on('recupCodeQCM')
def recupCodeQCM(code):
    idProf = session['idU']
    checkCodeQcmProf[idProf] = code
    print("check prof = ", checkCodeQcmProf)




##########################################################

@app.route("/stats", methods=['GET'])            # Route pour les statistiques
def stats():
    title="Statistiques"
    if 'nomU' not in session:                   # Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    return render_template("statistiques.html",title=title,page="Stats")

@app.route("/modifierQCM/<string:id>", methods=['POST', 'GET'])       # Route pour modifier un qcm
def modifierQCM(id):
    title='Modification QCM'
    if 'nomU' not in session:                   # Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    qcm_modif=QCM.query.get_or_404(id)                                # Récupération du qcm à modifier selon l'id selectioné 

    if request.method == 'POST':
        nom_qcm=request.form["nomQcm"]                                # Récupération du nouveau nom pour le qcm
        questions=request.form.getlist("questions")                   # Et des nouvelles questions

        try:
            qcm_modif.Nom=nom_qcm                                     # Nouveau nom
            Contient.query.filter_by(RidQCM=qcm_modif.idQCM).delete() # Suppression des anciennes relations
            for key,value in request.form.items():                    # Nouvelles relations
                if value=='on':
                    new_contient=Contient(RidQCM=qcm_modif.idQCM,RidQ=key)
                    db.session.add(new_contient)
            db.session.commit()
        except:
            return 'Erreur dans la modification du QCM'

        return redirect("/listeQCM")        # Redirection vers la liste des qcm
    else:
        LQ = db.session.query(Question).filter(Question.idU == session['idU']).all()    # Affichage des questions du qcm
        questions=Question.query.join(Contient).filter(Question.idU==session['idU'],Contient.RidQCM==id).all()  #Avec les relations
        return render_template("qcm/modifQCM.html",title=title,page="ListeQCM",QCMmodif=qcm_modif,ListesQuestions=LQ,questions=questions)

@app.route("/supprimerQCM/<string:id>")          # Route pour supprimer un qcm
def supprimerQCM(id):
    if 'nomU' not in session:                    # Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    qcm_modif=QCM.query.get_or_404(id)           # Récupération du qcm à supprimer selon l'id selectioné 

    try :
        Contient.query.filter_by(RidQCM=qcm_modif.idQCM).delete()    # Suppression des relations liées au qcm
        QCM.query.filter(QCM.idU==session['idU'], QCM.idQCM==qcm_modif.idQCM).delete() #Suppression du qcm
        db.session.commit()
    except :
        return "Erreur dans la suppréssion du QCM"
    return redirect("/listeQCM")                 # Redirection vers la liste des qcm

question_ouverte_nom = ""               # Variable globale contenant le titre de la question ouverte
reponses_par_prof = {}                  # Variable globale contenant les réponses des étudiants par profs

@app.route("/question-ouverte", methods=['POST', 'GET'])    # Route pour lancer une question ouverte
def question_ouverte():
    if 'nomU' not in session:                   # Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    global question_ouverte_nom
    nomProf = session['nomU']              # Récupération du nom du professeur dans la session
    
    if request.method == 'POST':
        if 'question-ouverte' in  request.form:             # Envoie du titre de la question
            question_ouverte_nom = request.form['question-ouverte']
            return render_template("ouverte/questionOuverte.html",title='Question ouverte',page="QuestionOuverte",question_ouverte=question_ouverte_nom)
        else:                                               # Affichage des réponses
            return render_template("ouverte/nuage.html",title='Nuage de réponses',page="QuestionOuverte")
    else:   
        reponses_par_prof[nomProf] = []        # Reset des données de l'enseignant pour une nouvelle question
        print(reponses_par_prof)
        print("on reset !")
        return render_template("ouverte/questionOuverte.html",title='Question ouverte',page="QuestionOuverte")

import language_tool_python
import spacy

tool = language_tool_python.LanguageTool('fr')
nlp = spacy.load('fr_core_news_sm')

@app.route("/reponse-ouverte", methods=['POST', 'GET'])    # Route pour répondre à la question ouverte
def reponse_ouverte():
    if 'nomU' not in session:                   # Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))

    if request.method == 'POST':
        nomProf = request.form['nomP']          # On entre le nom du professeur à qui on répond

        ##########################################################
        # Vérification si l'élève est élève du professeur 
        idEleve = session['idU']                                                           # On récupère l'id de session de l'élève
        idProf = db.session.query(Utilisateur).filter(Utilisateur.nomU == nomProf).first() # On récupère l'id du prof à partir du nom entré
        print(idEleve)
        print(idProf.idU)                                     # On vérifie qu'ils sont dans la même "classe"
        filterEleve = db.session.query(Classe).filter(Classe.idCE==idEleve).filter(Classe.idCU==idProf.idU).first()
        print(filterEleve)
        ##########################################################

        if filterEleve!=None:             # Si on trouve une classe
            proposition = request.form['reponse']    # proposition écrite par un étudiant
            correcteur = tool.correct(proposition)   # Correction grammaticale du/des mot(s)
            minuscule = correcteur.lower()           # Mise en minuscule du/des mot(s)
            singulier = nlp(minuscule)               # Mise au singulier du/des mot(s)

            mots = ""                        # Initalisation de la chaine de caractères
            for mot in singulier:            # Pour chaque mot de singulier, on ajout à "mots" le singulier du mot
                mots += mot.lemma_+" "
            mots = mots[:-1]                 # On supprime l'espace en trop en bout de chaine

            dejaLa = False                           # Si le mot est déja la

            if nomProf not in reponses_par_prof.keys():  # Si le prof n'a pas lancé de question ouverte
                flash("Veuillez patienter, la question va bientôt démarrer")
                return redirect("/")
            else:
                for r in reponses_par_prof[nomProf]:      # Pour chaque réponse
                    if mots in r.keys():                  # Si on voit que le mot est déja la
                        r[mots] += 1                      # On augmente 
                        dejaLa = True
                if not dejaLa:                            # Si le mot est nouveau
                    reponses_par_prof[nomProf].append({mots:1}) # On l'ajoute
                print(reponses_par_prof)
                return redirect("/")
        else:
            flash("vous n'êtes pas élève de ce professeur")
            return redirect("/")
    else:
        return render_template("ouverte/reponseOuverte.html",title='Réponse ouverte',page="ReponseOuverte")

reponses_par_prof_2 = {}

@app.route("/donnees-reponses",methods=['GET'])  # Route des données
def donnees_reponses():
    if 'nomU' not in session:                   # Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))

    nomProf = session['nomU']
    reponses_ouvertes_2 = {"mots": [],"titre":question_ouverte_nom}
    reponses_par_prof_2[nomProf] = []          # On initialise un dictionnaire vide pour pouvoir récuperer les données correctement

    for r in reponses_par_prof[nomProf]:         # Création de l'objet adapté pour le nuage de mots
        for cle, valeur in r.items():
            ajustement = {"x": cle, "value": valeur}
            reponses_ouvertes_2["mots"].append(ajustement)

    reponses_par_prof_2[nomProf].append(reponses_ouvertes_2)
    
    return reponses_par_prof_2                # On envoie les données sur la route

@socket.on('testQP')
def testQP():
    print("success mon frere")

if __name__ == '__main__':
    socket.run(app, host='0.0.0.0', port=5000, debug=True)