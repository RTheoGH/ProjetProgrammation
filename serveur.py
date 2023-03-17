from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.datastructures import MultiDict, ImmutableMultiDict
from werkzeug.security import generate_password_hash,check_password_hash
import random
import string
import csv
from datetime import datetime

app = Flask(__name__)                                         #Création de app, instance de Flask
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'                      #Clé de session (utilisateurs)

from bdd import *                                             #Importation de la base de donnée depuis bdd.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projet.db' #Création du fichier de la base de donnée
db.init_app(app)

# with app.app_context(): 
#     idq = QCM.query.first()
#     print("idq = " , idq)
#     envoyerTest = EnvoyerQCM(idQCM = idq.idQCM,idU = idq.idU)
#     print("envoyerTest = ",envoyerTest)
#     db.session.add(envoyerTest)
#     db.session.commit()
    # db.drop_all()
    # db.create_all()
# si le "with" n'est pas commenté:
#       si vous rechargez le serveur sans vous deconnecter, une erreur arrive au niveau de l'accueil,
#          utilisez la route /deconnexion pour corriger le probleme

nombreIdQuestion=0               #Variables utilisés pour 
nombreIdCheck=0                  #la génération de réponses
nombreIdQCM=0

def createId():                  #Fonction appelée à chaque fois qu'on a besoin de générer un nouvel id
    id=""
    for _ in range(8):
        id+=(random.choice((string.ascii_letters)+("0123456789")))
    return id

@app.route("/")                  #Route principale
def index():                                         #'page' est la référence de chaque page web actuelle
    title='Accueil'
    if 'nomU' not in session :                       #Accueil si aucun utilisateur n'est connecté
        return render_template("accueil/index.html",title=title,page="Menu") #coloré en rouge dans la barre de navigation
    else:
        if session['role']=='enseignant':            #Accueil si l'utilisateur connecté est un enseignant
            enseignantCO= db.session.query(Utilisateur).filter(Utilisateur.idU==session['idU']).first()
            return render_template("accueil/index.html",title=title,page="Menu",idU=enseignantCO.idU)
        elif session['role']=='etudiant':            #Accueil si l'utilisateur connecté est un etudiant
            etudiantCO = db.session.query(Etudiant).filter(Etudiant.numeroEtu==session['idU']).first()
            return render_template("accueil/index.html",title=title,page="Menu",numeroEtu=etudiantCO.numeroEtu)

@app.route("/espEnseignant")                         #Espace dédié aux enseignants
def espEnseignant():
    title='Espace Enseignant'
    return render_template("accueil/espEnseignant.html",title=title,page="Menu")

@app.route("/espEtudiant")                           #Espace dédié aux etudiants
def espEtudiant():
    title='Espace Etudiant'
    return render_template("accueil/espEtudiant.html",title=title,page="Menu")

@app.route("/creationCompteEnseignant",methods = ['POST', 'GET'])   #Route pour créer un compte utilisateur
def creationCompteEnseignant():
    title='Creation de compte'
    if request.method == 'POST':
        nomUtilisateur = request.form['creationNom']                #generate_password_hash est une methode de
        mdpUtilisateur = request.form['creationMdp']                #werkzeug.security pour crypter les mot de passes
        new_utilisateur = Utilisateur(nomU=nomUtilisateur,passU=generate_password_hash(mdpUtilisateur, method='pbkdf2:sha256', salt_length=16))

        try:
            db.session.add(new_utilisateur)               #Création du nouveau compte
            db.session.commit()
            return redirect(url_for("espEnseignant"))
        except:
            return 'Erreur lors de la création du compte'
    else: 
        return render_template("compte/creationCompteEnseignant.html",title=title,page="Menu")

@app.route("/listeUtilisateurs",methods = ['GET'])        #Cette route est uniquement technique pour pouvoir
def listeUtilisateurs():                                  #visualiser les utilisateurs en aucun cas elle doit
    title='PRIVATE'                                       #etre accessible via une redirection ou autre.
    if 'nomU' not in session or session['nomU']!='ADMIN': 
        flash("Vous n'avez pas les droits pour accéder à cette page")  #Si vous souhaitez néanmoins accéder à la
        return redirect(url_for('index'))                              #page, créez un compte 'ADMIN' puis
    utilisateurs = db.session.query(Utilisateur).all()                 #connectez vous avec.
    return render_template("liste/lUtilisateurs.html",lUtilisateurs=utilisateurs,title=title,page='ListeUtilisateurs')

@app.route("/listeEtudiants",methods=['POST','GET'])
def listeEtudiants():
    title='Etudiants'
    if 'nomU' not in session:                                           #Sécurité pour éviter d'aller sur une page
        flash("Connectez vous ou créer un compte pour accéder à cette page") #sans se connecter
        return redirect(url_for('index'))
    if request.method == 'POST':
        if 'fichierEtu' in request.files:
            fichierCsv = request.files['fichierEtu']                    #récupération du fichier depuis l'html
            if fichierCsv.filename != '':
                contenuCsv = []                                               #Contenu du fichier sous forme de liste de listes
                decoded_file = fichierCsv.read().decode('iso-8859-1')         #Decodeur (iso equivalent de utf-8)
                reader = csv.reader(decoded_file.splitlines(), delimiter=';') #Début de la lecture du fichier
                next(reader)                                                  #on ignore la ligne avec les titres des colonnes
                for ligne in reader:
                    contenuCsv.append(ligne)

                for eleve in contenuCsv:                                    #Ajout des elèves dans la base de donnée
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
            nomEtudiant=request.form['nomEtu']                              #Ajout d'un elève dans la base de donnée
            prenomEtudiant=request.form['prenomEtu']                        #manuellement
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

@app.route("/retirerEtu/<int:id>")                    #Route pour retirer un étudiant
def retirerEtu(id):
    if 'nomU' not in session:                           #Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    etudiantMoins = Etudiant.query.get_or_404(id)                          #Récupération étudiant
    classeMoins = db.session.query(Classe).filter(Classe.idCE==id).first() #Récupération classe
    
    try:
        db.session.delete(classeMoins)                  #Suppression classe
        db.session.delete(etudiantMoins)                #Suppression etudiant
        db.session.commit()                             #Envoi des modifications à la base de données
        return redirect(url_for('listeEtudiants'))          #Redirection vers la liste d'étudiants
    except:
        return 'Erreur lors de la suppression'

@app.route("/connexionEnseignant",methods=['POST','GET'])           #Route pour se connecter
def connexionEnseignant():
    title='Connexion Enseignant'
    if request.method == 'POST':
        testLogin = db.session.query(Utilisateur).filter(Utilisateur.nomU == request.form['nomU']).first()
        if testLogin is None:
            flash('Nom invalide')                                        #Il faut d'abord crée un compte
            return redirect(url_for('connexionEnseignant'))              #check_password_hash est une methode de
        if check_password_hash(testLogin.passU,request.form['passU']):   #werkzeug.security pour verifier qu'un mot de passe
            session['nomU'] = request.form['nomU']                       #correspond avec le cryptage
            session['idU'] = testLogin.idU
            session['role'] = "enseignant"
        else:
            flash('Mot de passe invalide')             
            return redirect(url_for('connexionEnseignant'))  
        return redirect(url_for("index"))              
    else:                       
        return render_template("compte/connexionEnseignant.html",title=title,page="Menu")

@app.route("/connexionEtudiant",methods=['POST','GET'])           #Route pour se connecter
def connexionEtudiant():
    title='Connexion Etudiant'
    if request.method == 'POST':
        testLogin = db.session.query(Etudiant).filter(Etudiant.nomEtu == request.form['nomU']).first()
        if testLogin is None:
            flash('Nom invalide')             #Il faut d'abord crée un compte
            return redirect(url_for('connexionEtudiant'))  
        if check_password_hash(testLogin.mdpEtu,request.form['passU']): #Vérifie que le mdp correspond
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

@app.route("/modifMdp/<int:id>",methods=['POST','GET'])          #Route pour modifier son mot de passe
def modifMdp(id):
    title='Modification Mot de passe'
    if 'nomU' not in session :                                          #Sécurité pour éviter d'aller sur une page
        flash("Connectez vous ou créer un compte pour accéder à cette page") #sans se connecter
        return redirect(url_for('index'))
    if request.method == 'POST':
        mdpActuel=request.form['mdpActu']            #Mot de passe actuel
        newMdp=request.form['nMdp']                  #Nouveau mot de passe
        if session['role']=='etudiant':                                #Pour les étudiants
            mdpAModif = Etudiant.query.get_or_404(id)
            print("numero a modifier:",mdpAModif)
            if check_password_hash(mdpAModif.mdpEtu,mdpActuel):        #Verifie la correspondance mdp entré/mdp actuel
                mdpAModif.mdpEtu = generate_password_hash(newMdp, method='pbkdf2:sha256', salt_length=16) #Attribue le nouveau mdp
                # print("j'attribue le nouveau mot de passe ! :",newMdp)
                db.session.commit()
                flash("Mot de passe modifié avec succès")
                return redirect(url_for("index"))
            else:
                flash("Mot de passe actuel incorrect")
                # print("tu as entré :",mdpActuel)
                return redirect(url_for("index"))
        elif session['role']=='enseignant':                            #Pour les enseignants
            mdpAModif = Utilisateur.query.get_or_404(id)
            if check_password_hash(mdpAModif.passU,mdpActuel):
                print("hello ?")                                       #Verifie la correspondance mdp entré/mdp actuel
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

@app.route("/deconnexion")                        #Route de deconnexion
def deconnexion():                                #Retire l'utilisateur de la session
    session.pop('nomU',None)
    return redirect(url_for("index"))

@app.route("/ajout",methods = ['POST', 'GET'])    #Route pour ajouter une question
def ajout():
    title='Ajout'
    if 'nomU' not in session :                                          #Sécurité pour éviter d'aller sur une page
        flash("Connectez vous ou créer un compte pour accéder à cette page") #sans se connecter
        return redirect(url_for('index'))
    if session['role'] != 'enseignant' :                                     #si vous n'êtes pas prof
        flash("Vous n'avez pas les droits nécéssaires")           
        return redirect(url_for('index'))

    if request.method == 'POST':                  #Recup question du formulaire
        question = request.form['question']       #Création nouvelle question avec enoncé correspondant  
        
        idQuest = createId()
        while idQuest in db.session.query(Question.idQ):
            idQuest = createId()

        new_question = Question(idQ=idQuest,enonce=question,idU=session['idU'])
        
        recupForm = request.form.getlist("reponse")     #On récupère la liste des questions
        if recupForm == []:
            # rep_num1 = request.form["rep_num1"]
            # rep_num2 = request.form["rep_num2"]
            # rep_num = float(rep_num1) + float(float(rep_num2)*0.01)
            rep_num = request.form["Rep_num"]

        #try:
        db.session.add(new_question)                #Ajout question -> base de donnée            
        db.session.commit()                         #Envoie des changements
        idQuestion = db.session.query(Question.idQ).filter(Question.enonce == question).first()
        if recupForm == []:
            db.session.add(Reponse(reponse=rep_num,correction = 1,estNumerique = True,idQ=idQuestion[0]))
            
        listeOn = []                              
        for key,value in request.form.items():      #Pour chaque item du formulaire
            if value == 'on':
                listeOn.append(int(key))            #Attribut d'id pour la question
        
        for rep in recupForm:
            reponseAjouter = 0
            if (recupForm.index(rep)+1) in listeOn: #On ajoute réponse juste
                reponseAjouter = Reponse(reponse= rep,correction = 1,idQ =idQuestion[0])
                db.session.add(reponseAjouter)
            else:                                   #On ajoute réponse fausse
                reponseAjouter = Reponse(reponse= rep,correction = 0,idQ =idQuestion[0])
                db.session.add(reponseAjouter)       
        db.session.commit()
        

        print("idquestion de 0 = ",idQuestion[0]," id question en tout = ",idQuestion)
        print(db.session.query(Reponse.reponse).filter(Reponse.idQ == idQuestion[0]).all())#test
        selected_tags = request.form.getlist('tag') #On récupère la liste des étiquettes
        for tag_id in selected_tags:
            new_assos = Associe(RidE=tag_id,RidQ=new_question.idQ) #On crée l'association entre question
            db.session.add(new_assos)                              #et étiquette
            db.session.commit()                     #Envoie des changements
        print("reponse.exe = ",db.session.query(Reponse.reponse).filter(Reponse.idQ==idQuestion[0]).all())
        return redirect(url_for('lQuestion'))       #Redirection vers la liste des questions
        # except:
        #    return 'Erreur création de la question'
    else:
        return render_template("question/ajoutQuestion.html",title=title,page="Créer")

@app.route("/creationEtiquettes",methods=['GET','POST']) #Route pour créer une étiquette
def creationEtiquettes():
    title='Etiquette'
    if 'nomU' not in session:                            #Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    if request.method == 'POST':
        nom = request.form['nom']
        new_etiquette = Etiquette(nom=nom,idU=session['idU'])

        try :
            db.session.add(new_etiquette)                #Ajout de l'étiquette
            db.session.commit()
            print(Etiquette.query.all(),new_etiquette.nom,new_etiquette.idE)
            return redirect(url_for('creationEtiquettes'))
        except:
            return 'Erreur : route /creationEtiquettes'
    else :
        ToutEtiq = db.session.query(Etiquette).filter(Etiquette.idU==session['idU']).all()
        return render_template("question/creationEtiquettes.html",title=title,page="Etiquettes",etiqs=ToutEtiq)

@app.route("/suppEtiquettes",methods=['GET','POST'])     #Route pour supprimer une étiquette
def suppEtiquettes():
    title='Etiquette'
    if 'nomU' not in session:                            #Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    if request.method == 'POST':
        nom = request.form['nom']
        
        try :                                            #On associe avec l'étiquette puis on sélectionne l'étiquette en question
            test = db.session.query(Associe).join(Etiquette,Associe.RidE == Etiquette.idE).filter(Etiquette.nom == nom,Etiquette.idU==session['idU']).all()
            etiq = db.session.query(Etiquette).filter(Etiquette.nom==nom,Etiquette.idU==session['idU']).first()
            for associe in test:
                db.session.delete(associe)
                db.session.commit()
            else:
                print("Etiquette not found")             #Si on ne trouve pas l'étiquette
            db.session.delete(etiq)
            db.session.commit()
            return redirect(url_for('creationEtiquettes'))
        except:
            return 'Erreur : route /suppEtiquettes'
    else :
        return render_template("question/creationEtiquettes.html",title=title,etiqs=ToutEtiq)

@app.route("/modifEtiquettes",methods=['GET','POST'])     #Route pour modifier une étiquette
def modifEtiquettes():
    title='Etiquette'
    if 'nomU' not in session:                             #Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    if request.method == 'POST':
        nom = request.form['nom']
        etiqIde = request.form['etiqAmodif']              #Recupere l'étiquette à modifier

        try :                                             #Sélectionne l'étiquette en question
            etiqAmodif = db.session.query(Etiquette).filter(Etiquette.idE==etiqIde)
            etiqAmodif.update({"nom" : nom })             #Change le nom
            db.session.commit()
            return redirect(url_for('creationEtiquettes'))
        except:
            return 'Erreur : route /modifEtiquettes'
    else :
        return render_template("question/creationEtiquettes.html",title=title,etiqs=ToutEtiq)

@app.route("/creerQuestion",methods=['GET','POST'])       #Route pour afficher les étiquettes sur ajoutQuestion
def creerQ():
    title='Ajout'
    if 'nomU' not in session:                             #Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    etiquettes = db.session.query(Etiquette).filter(Etiquette.idU==session['idU']).all()
    return render_template('question/ajoutQuestion.html',title=title,etiquettes=etiquettes, page="Créer")

@app.route("/plusDeReponse",methods = ['GET'])          #Route qui ajoute une réponse sur ajoutQuestion
def plusDeReponse():
    global nombreIdQuestion,nombreIdCheck               #Déclaration variables globales nombreIdQuestion, nombreIdCheck
    nombreIdQuestion+=1                                 #Incrémentation de nombreIdQuestion et nombreIdCheck
    nombreIdCheck+=1                                    #de 1 (pour avoir des id différent pour chaque objet)
    return render_template('partials/nouvelleReponse.html',IdBouton=nombreIdQuestion,IdCheck=nombreIdCheck)
    # Rendu template 'partials/nouvelleReponse.html' et passage des paramètres IdBouton et IdCheck

@app.route("/supprimer_bouton", methods=['DELETE'])     #Route qui supprime une réponse sur ajoutQuestion
def supprimer_bouton():
    id = request.json['id']
    return 'SUCCES'

@app.route("/lQuestion",methods = ['GET'])              #Route vers la liste de questions de l'utilisateur
def lQuestion():
    title='Bibliothèque'
    if 'nomU' not in session:                           #Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))               #Sélection des questions et étiquettes
    etiquettes = db.session.query(Etiquette).filter(Etiquette.idU==session['idU']).all()
    questions = db.session.query(Question).filter(Question.idU==session['idU']).all()
    return render_template("liste/lQuestion.html",title=title,etiquettes=etiquettes,lquestion=questions,page="ListeQuestions")

@app.route("/filtre",methods = ['GET','POST'])          #Route de filtrage des questions de l'utilisateur
def filtre():
    title='Bibliothèque'
    etiquettes = db.session.query(Etiquette).filter(Etiquette.idU==session['idU']).all()
    tags = request.form['tag']
    if request.method == 'POST':                        #Affiche les questions avec les tags sélectionnés
        questionAffiche = db.session.query(Question).join(Associe, Associe.RidQ == Question.idQ)\
            .join(Etiquette, Etiquette.idE == Associe.RidE).filter(Etiquette.idE == tags,Etiquette.idU==session['idU']).all()
        return render_template("liste/lQuestion.html",title=title,etiquettes=etiquettes, lquestion=questionAffiche, page="ListeQuestions")

@app.route("/modifier/<string:id>",methods=['POST','GET']) #Route pour modifier une question de l'utilisateur
def modifier(id):
    title='Modification Question'
    if 'nomU' not in session:                           #Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    selected_tags = request.form.getlist('tag')
    questionModif = Question.query.get_or_404(id)       #Recup question avec id correspondant, erreur sinon
    reponseModif = Reponse.query.filter(Reponse.idQ==questionModif.idQ).all() #Recup les reponses de la question
    ToutAssoc = db.session.query(Associe).filter(Associe.RidQ==questionModif.idQ).all()
    
    if request.method == 'POST':
        questionModif.enonce = request.form['question'] #Modification de l'enoncé de la question
        for r in reponseModif:                          #Pour chaque reponse, modifie tout
            r.reponse = request.form['R'+str(r.idR)]
        
        try:
            db.session.query(Associe).filter(Associe.RidQ == id).delete()
            db.session.commit()                         #Envoi des modifications à la base de données
            for tag_id in selected_tags:
                new_assos = Associe(RidE=tag_id,RidQ=questionModif.idQ)
                db.session.add(new_assos)
                db.session.commit()  
            return redirect(url_for('lQuestion'))       #Redirection vers la page de liste des questions
        except:
            return 'Erreur de modification'             #Renvoi message erreur en cas d'échec de la modification
    else:
        etiquettes = db.session.query(Etiquette).filter(Etiquette.idU==session['idU']).all()
        return render_template("question/modifQuestion.html",title=title,enonce=questionModif.enonce,\
            idQ=questionModif.idQ,reponses=reponseModif,etiquettes=etiquettes,page="ListeQuestions")

@app.route("/supprimer/<string:id>")                    #Route pour supprimer une question de l'utilisateur
def supprimer(id):
    if 'nomU' not in session:                           #Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    questionSupp = Question.query.get_or_404(id)        #Récupération question correspondant id, sinon erreur
    toutAssocie = db.session.query(Associe).all()    
    reponseSupp = db.session.query(Reponse.idR).filter(Reponse.idQ==id).all()

    try:
        for key in reponseSupp:                         #Supprime toutes les réponses
            Asupp = Reponse.query.get_or_404(key)
            db.session.delete(Asupp)
        for assoc in toutAssocie :                      #Supprime toutes les associations
            if(assoc.RidQ==id):
                db.session.delete(assoc)
                db.session.commit()
        db.session.delete(questionSupp)                 #Suppression question de la base de données
        db.session.commit()                             #Envoi des modifications à la base de données
        return redirect(url_for('lQuestion'))           #Redirection vers la page de liste des questions
    except:
        return 'Erreur lors de la suppression de la question'
        #Renvoi message d'erreur si échec de la suppression de la question

@app.route("/listeQCM",methods = ['GET','POST'])      #Route qui genere le qcm
def listeQCM():
    title='Vos QCM'
    if 'nomU' not in session:                   #Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    
    if request.method == 'POST':                #Création de QCM
        idQcm = createId()
        while idQcm in db.session.query(QCM.idQCM):
                idQcm = createId()
        nomQcm = request.form['nomQcm']
        new_QCM = QCM(idQCM=idQcm,Nom=nomQcm,idU=session['idU'])

        try : 
            db.session.add(new_QCM)
            db.session.commit()
        except : 
            return 'Erreur dans la création du QCM'
        for key, value in request.form.items():                #Association du QCM à ses Questions
            if value == 'on':                                  #key=idQuestion ; value=valeur du commutateur
                new_contient = Contient(RidQCM=idQcm,RidQ=key)

                try :
                    db.session.add(new_contient)
                    db.session.commit()
                except :
                    return "Erreur de création du lien 'contient' entre Qcm et Question"
        return redirect("http://127.0.0.1:5000/listeQCM")
    else:
        listeQCM = db.session.query(QCM).filter(QCM.idU==session['idU']).all()
        LQ = db.session.query(Question).filter(Question.idU==session['idU']).all()
        return render_template("liste/lQCM.html",title=title,listeQCM=listeQCM,ListesQuestions=LQ,page="ListeQCM")

@app.route("/afficheQCM/<string:id>")        #Affichage des questions du Qcm avec leurs réponses
def afficheQCM(id):                          #Rq: le [0] sert à isoler la chaine de char, puisque la requête renvoie un objet 
    nomQcm = db.session.query(QCM.Nom).filter(QCM.idQCM==id).first()[0]   
    title = nomQcm 
    listeIdQuestions = db.session.query(Contient.RidQ).filter(Contient.RidQCM==id).all() #Liste des idQuestions cochées
    checked_questions = []                          #Liste des questions du QCM (objets Question entiers)
    checked_reponses = []                           #Leurs reponses respectives (liste de listes)
    for idQuestion in listeIdQuestions:             #Pour chaque idQuestion, on récupère
        idQuestion = idQuestion[0]
        objetQuestion = db.session.query(Question).filter(Question.idQ==idQuestion).first()
        checked_questions.append(objetQuestion)     #l'objet Question entier
        listeReponse = db.session.query(Reponse).filter(Reponse.idQ==idQuestion).all()
        if (listeReponse[0].estNumerique):
            checked_reponses.append([])
        else:
            checked_reponses.append(listeReponse)       #et les réponses correspondantes à cette question
    return render_template("qcm/affichage.html",title=title,nomQcm=nomQcm,listeQuestions=checked_questions,\
        listeReponses=checked_reponses,len=len(checked_questions),page="ListeQCM")

@app.route("/RepondreQCM/<int:i>",methods =["POST","GET"])
def RepondreQCM(i):
    title='Repondez aux questions'
    if 'nomU' not in session:                   #Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    if request.method == "POST":
        reponse = request.form.getlist('reponse_choix')
        reponseN = request.form.getlist("reponse_num")
        question = request.form.getlist("question")
        i = i+1
        idq = EnvoyerQCM.query.first()
        ListeQuestionsQcm = db.session.query(Question).join(Contient,Contient.RidQCM == idq.idQCM).all()
        ListeReponseQcm = []
        for key in ListeQuestionsQcm:
            add = db.session.query(Reponse).filter(key.idQ == Reponse.idQ).all()
            ListeReponseQcm.append(add)
        lena = len(ListeQuestionsQcm) 
        # prepare la bdd
        idE = session['idU']
        preE = session['preU']
        nomE = session['nomU'] 
        dateA = str(datetime.now())
        idQbdd = idq.idQCM
        if i == lena:
            return redirect(url_for("index")) 
        return render_template("wooclap/RepondreQCM.html",page="RepondreQCM",nomQcm = "test",lena=lena,ListeReponseQcm = ListeReponseQcm,ListeQuestionsQcm = ListeQuestionsQcm,i= i)
    else:
        idq = EnvoyerQCM.query.first()
        if idq == None:
            return render_template("wooclap/RepondreQCM.html",page="RepondreQCM",nomQcm = "test",lena=0,ListeReponseQcm = [],ListeQuestionsQcm = [],i= 0)
        i= 0
        idq = EnvoyerQCM.query.first()
        ListeQuestionsQcm = db.session.query(Question).join(Contient,Contient.RidQCM == idq.idQCM).all()
        ListeReponseQcm = []
        for key in ListeQuestionsQcm:
            add = db.session.query(Reponse).filter(key.idQ == Reponse.idQ).all()
            ListeReponseQcm.append(add)
        lena = len(ListeQuestionsQcm)  
        return render_template("wooclap/RepondreQCM.html",page="RepondreQCM",nomQcm = "test",lena=lena,ListeReponseQcm = ListeReponseQcm,ListeQuestionsQcm = ListeQuestionsQcm,i= i)

@app.route("/envoyerEnonce",methods = ["POST","GET"])
def caster():
    title='Envoyer un énoncé'
    if 'nomU' not in session:                   #Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    if request.method == "POST":
        idElementCaste = request.form['radio']
        if 'question' in request.form:
            questions = db.session.query(Question).filter(Question.idQ==idElementCaste).all()
        else:
            questions=[]
            liQuestions = db.session.query(Contient.RidQ).filter(Contient.RidQCM==idElementCaste).all()
            for quest in liQuestions:                
                idQ = db.session.query(Question).filter(Question.idQ==quest[0]).all()
                questions.append(idQ[0])
        return render_template('wooclap/casterEnonce.html',title=title,idElement=idElementCaste,listeQuestions=questions)

    else:
        listeQuestions = db.session.query(Question).filter(Question.idU==session['idU']).all()
        listeQCM = db.session.query(QCM).filter(QCM.idU==session['idU']).all()
        return render_template("wooclap/envoyerEnonce.html",title=title,listeQCM=listeQCM,listeQuestions=listeQuestions,page = "EnvoyerEnonce")

@app.route("/majRepondre",methods = ["POST","GET"])
def majRepondre():
    if 'nomU' not in session:                   #Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    
    # Enonce = db.session.query(EnvoyerQCM).all()
    # return Enonce

@app.route("/modifierQCM/<string:id>", methods=['POST', 'GET'])
def modifierQCM(id):
    title='Modification QCM'
    qcm_modif=QCM.query.get_or_404(id)

    if request.method == 'POST':
        nom_qcm=request.form["nomQcm"]
        questions=request.form.getlist("questions")

        try:
            qcm_modif.Nom=nom_qcm                                   #Nouveau nom
            Contient.query.filter_by(RidQCM=qcm_modif.idQCM).delete() #Suppression des anciennes relations
            for key,value in request.form.items():                   #Nouvelles relations
                if value=='on':
                    new_contient=Contient(RidQCM=qcm_modif.idQCM,RidQ=key)
                    db.session.add(new_contient)
            db.session.commit()
        except:
            return 'Erreur dans la modification du QCM'

        return redirect("http://127.0.0.1:5000/listeQCM")
    else:
        LQ = db.session.query(Question).filter(Question.idU == session['idU']).all()
        questions=Question.query.join(Contient).filter(Question.idU==session['idU'],Contient.RidQCM==id).all()
        return render_template("qcm/modifQCM.html",title=title,page="ListeQCM",QCMmodif=qcm_modif,ListesQuestions=LQ,questions=questions)

@app.route("/supprimerQCM/<string:id>")
def supprimerQCM(id):
    title='supprimer QCM'
    qcm_modif=QCM.query.get_or_404(id)
    try :
        Contient.query.filter_by(RidQCM=qcm_modif.idQCM).delete()
        QCM.query.filter(QCM.idU==session['idU'], QCM.idQCM==qcm_modif.idQCM).delete()
        db.session.commit()
    except :
        return "Erreur dans la suppréssion du QCM"
    return redirect("http://127.0.0.1:5000/listeQCM")

@app.route("/stats", methods=['GET'])
def stats():
    return render_template("statistiques.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)