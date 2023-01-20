from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.datastructures import MultiDict, ImmutableMultiDict

app = Flask(__name__)                                         #Création de app, instance de Flask
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'                      #Clé de session (utilisateurs)

from bdd import *                                             #Importation de la base de donnée depuis bdd.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projet.db' #Création du fichier de la base de donnée
db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

nombreIdQuestion=0               #Variables utilisés pour 
nombreIdCheck=0                  #la génération de réponses

@app.route("/")                  #Route principale
def index():                                         #'page' est la référence de chaque page web actuelle
    return render_template("index.html",page="Menu") #coloré en rouge dans la barre de navigation   

@app.route("/creationCompte",methods = ['POST', 'GET'])   #Route pour créer un compte utilisateur
def creationCompte():
    if request.method == 'POST':
        nomUtilisateur = request.form['creationNom']
        mdpUtilisateur = request.form['creationMdp']
        new_utilisateur = Utilisateur(nomU=nomUtilisateur,passU=mdpUtilisateur)

        try:
            db.session.add(new_utilisateur)               #Création du nouveau compte
            db.session.commit()
            return redirect(url_for("index"))
        except:
            return 'Erreur lors de la création du compte'
    else: 
        return render_template("creationCompte.html")

@app.route("/listeUtilisateurs",methods = ['GET'])        #Cette route est uniquement technique pour pouvoir
def listeUtilisateurs():                                  #visualiser les utilisateurs en aucun cas elle doit
    if 'nomU' not in session or session['nomU']!='ADMIN': #etre accessible via une redirection ou autre.
        flash("Vous n'avez pas les droits pour accéder à cette page")  #Si vous souhaitez néanmoins accéder à la
        return redirect(url_for('index'))                              #page, créez un compte 'ADMIN' puis
    utilisateurs = db.session.query(Utilisateur).all()                 #connectez vous avec.
    return render_template("lUtilisateurs.html",lUtilisateurs=utilisateurs,page='listeUtilisateurs')

@app.route("/connexion",methods=['POST','GET'])           #Route pour se connecter
def connexion():
    if request.method == 'POST':
        testLogin = db.session.query(Utilisateur).filter(Utilisateur.nomU == request.form['nomU']).first()
        # if request.form['nomU'] == request.form['passU']:   #ancienne méthode pour vérifier si nom=mdp
        if testLogin is None:
            flash('Nom ou mot de passe invalide')             #Il faut d'abord crée un compte
            return redirect(url_for('connexion'))             
        if request.form['passU'] == testLogin.passU:          #Vérifie que le mdp de l'utilisateur correspond
            session['nomU'] = request.form['nomU']            
            session['idU'] = testLogin.idU
        return redirect(url_for("index"))              
    else:                       
        return render_template("connexion.html")

@app.route("/deconnexion")                        #Route de deconnexion
def deconnexion():                                #Retire l'utilisateur de la session
    session.pop('nomU',None)
    return redirect(url_for("index"))

@app.route("/ajout",methods = ['POST', 'GET'])    #Route pour ajouter une question
def ajout():
    if 'nomU' not in session:                                           #Sécurité pour éviter d'aller sur une page
        flash("Connectez vous ou créer un compte pour accéder à cette page") #sans se connecter
        return redirect(url_for('index'))
    if request.method == 'POST':                  #Recup question du formulaire
        question = request.form['question']       #Création nouvelle question avec enoncé correspondant     
        new_question = Question(enonce=question,idU=session['idU'])
        recupForm = request.form.getlist("reponse")     #On récupère la liste des questions

        try:
            db.session.add(new_question)                #Ajout question -> base de donnée
            db.session.commit()                         #Envoie des changements
            listeOn = []                              
            for key,value in request.form.items():      #Pour chaque item du formulaire
                if value == 'on':
                    listeOn.append(int(key))            #Attribut d'id pour la question
            idQuestion = db.session.query(Question.idQ).filter(Question.enonce == question).first()
            for rep in recupForm:
                reponseAjouter = 0
                if (recupForm.index(rep)+1) in listeOn: #On ajoute réponse juste
                    reponseAjouter = Reponse(reponse= rep,correction = 1,idQ =idQuestion[0])
                    db.session.add(reponseAjouter)
                else:                                   #On ajoute réponse fausse
                    reponseAjouter = Reponse(reponse= rep,correction = 0,idQ =idQuestion[0])
                    db.session.add(reponseAjouter)       
            db.session.commit()
            selected_tags = request.form.getlist('tag') #On récupère la liste des étiquettes
            for tag_id in selected_tags:
                new_assos = Associe(RidE=tag_id,RidQ=new_question.idQ) #On crée l'association entre question
                db.session.add(new_assos)                              #et étiquette
                db.session.commit()                     #Envoie des changements
            return redirect(url_for('lquestion'))       #Redirection vers la liste des questions
        except:
            return 'Erreur création de la question'
    else:
        return render_template("ajoutQuestion.html",page="Créer")

@app.route("/creationEtiquettes",methods=['GET','POST']) #Route pour créer une étiquette
def creationEtiquettes():
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
        return render_template("creationEtiquettes.html",page="Etiquettes",etiqs=ToutEtiq)

@app.route("/suppEtiquettes",methods=['GET','POST'])     #Route pour supprimer une étiquette
def suppEtiquettes():
    if 'nomU' not in session:                            #Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    # print('avant suppression : ',Etiquette.query.all())
    if request.method == 'POST':
        nom = request.form['nom']
        
        try :                                            #On associe avec l'étiquette puis on sélectionne l'étiquette en question
            test = db.session.query(Associe).join(Etiquette,Associe.RidE == Etiquette.idE).filter(Etiquette.nom == nom,Etiquette.idU==session['idU']).all()
            etiq = db.session.query(Etiquette).filter(Etiquette.nom==nom,Etiquette.idU==session['idU']).first()
            # print('assos : ',assos,' tout :', db.session.query(Associe).all(), 'test join : ', test) 
            for associe in test:
                db.session.delete(associe)
                db.session.commit()
            else:
                print("Etiquette not found")
            db.session.delete(etiq)
            db.session.commit()
            # print('après suppression : ',Etiquette.query.all(),' association : ',Associe.query.all())
            return redirect(url_for('creationEtiquettes'))
        except:
            return 'Erreur : route /suppEtiquettes'
    else :
        return render_template("creationEtiquettes.html",etiqs=ToutEtiq)

@app.route("/modifEtiquettes",methods=['GET','POST'])     #Route pour modifier une étiquette
def modifEtiquettes():
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
        return render_template("creationEtiquettes.html",etiqs=ToutEtiq)

@app.route("/creerQuestion",methods=['GET','POST'])       #Route pour afficher les étiquettes sur ajoutQuestion
def creerQ():
    if 'nomU' not in session:                             #Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    etiquettes = db.session.query(Etiquette).filter(Etiquette.idU==session['idU']).all()
    return render_template('ajoutQuestion.html', etiquettes=etiquettes, page="Créer")

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
    #les questions ne sont pas encore stocké dans une variables donc ne peuvent pas être delete 
    # cursor = connection.cursor()
    # cursor.execute("DELETE FROM boutons WHERE id=%s", (id,))
    # connection.commit()
    # cursor.close()
    #qqc comme ça en bdd
    return 'SUCCES'

@app.route("/lquestion",methods = ['GET'])              #Route vers la liste de questions de l'utilisateur
def lquestion():
    if 'nomU' not in session:                           #Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))               #Sélection des questions et étiquettes
    etiquettes = db.session.query(Etiquette).filter(Etiquette.idU==session['idU']).all()
    questions = db.session.query(Question).filter(Question.idU==session['idU']).all()
    # tag = db.session.query(Etiquette, Associe).join(Associe, Etiquette.idE == Associe.RidE).join(Question, Question.idQ == Associe.RidQ).all()
    # print(tag)
    return render_template("lquestion.html",etiquettes=etiquettes,lquestion=questions,page="Consulter")

@app.route("/filtre",methods = ['GET','POST'])          #Route de filtrage des questions de l'utilisateur
def filtre():
    etiquettes = db.session.query(Etiquette).filter(Etiquette.idU==session['idU']).all()
    tags = request.form['tag']
    if request.method == 'POST':                        #Affiche les questions avec les tags sélectionnés
        questionAffiche = db.session.query(Question).join(Associe, Associe.RidQ == Question.idQ)\
            .join(Etiquette, Etiquette.idE == Associe.RidE).filter(Etiquette.idE == tags,Etiquette.idU==session['idU']).all()
        # print(questionAffiche)
        return render_template("lquestion.html",etiquettes=etiquettes, lquestion=questionAffiche, page="Consulter")

@app.route("/modifier/<int:id>",methods=['POST','GET']) #Route pour modifier une question de l'utilisateur
def modifier(id):
    if 'nomU' not in session:                           #Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    selected_tags = request.form.getlist('tag')
    questionModif = Question.query.get_or_404(id)       #Recup question avec id correspondant, erreur sinon
    ToutAssoc = db.session.query(Associe).filter(Associe.RidQ==questionModif.idQ).all()
    if request.method == 'POST':
        questionModif.enonce = request.form['question'] #Modification de l'enoncé de la question
        
        try:
            db.session.query(Associe).filter(Associe.RidQ == id).delete()
            db.session.commit()                         #Envoi des modifications à la base de données
            for tag_id in selected_tags:
                new_assos = Associe(RidE=tag_id,RidQ=questionModif.idQ)
                db.session.add(new_assos)
                db.session.commit()  
            return redirect(url_for('lquestion'))       #Redirection vers la page de liste des questions
        except:
            return 'Erreur de modification'             #Renvoi message erreur en cas d'échec de la modification
    else:
        etiquettes = db.session.query(Etiquette).filter(Etiquette.idU==session['idU']).all()
        return render_template("modifQuestion.html",enonce=questionModif.enonce,idQ=questionModif.idQ,etiquettes=etiquettes)

@app.route("/supprimer/<int:id>")                       #Route pour supprimer une question de l'utilisateur
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
        return redirect(url_for('lquestion'))           #Redirection vers la page de liste des questions
    except:
        return 'Erreur lors de la suppression de la question'
        #Renvoi message d'erreur si échec de la suppression de la question

@app.route("/QCM")                  #Route pour créer un qcm à partir des questions crée par l'utilisateur
def qcm():
    if 'nomU' not in session:       #Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    LQ = db.session.query(Question).filter(Question.idU==session['idU']).all()  #Récupération questions de la base de données
    print(LQ)
    return render_template("QCM.html",ListesQuestions=LQ,page="CréerQcm")

@app.route("/generate",methods = ['POST'])      #Route qui genere le qcm
def generate():
    if 'nomU' not in session:                   #Sécurité connexion
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    checked_checkboxes = [] 
    reponse_checkboxes = []                         #Initialisation liste pour stocker les questions cochées
    nomQcm = request.form['nomQcm']
    #insert sur qcm avec un idqcm : 
    #db.session.add(QCM(Nom = ))
    for key, value in request.form.items():
        if value == 'on':
            # checked_checkboxes.append(key)
            # Récupération de l'enoncé de la question correspondant à l'id reçu
            EL = db.session.query(Question).filter(Question.idQ == key,Question.idU==session['idU']).first()
            checked_checkboxes.append(EL)                                   #insert to dans contient idqcm(global a cette fun) et EL.idQ 
            ListeReponse = db.session.query(Reponse).filter(Reponse.idQ==key).all() #Ajout de l'enoncé à la liste des questions cochées
            reponse_checkboxes.append(ListeReponse)
    return render_template("Affichage.html", listereponse = reponse_checkboxes, listequestion=checked_checkboxes,len = len(checked_checkboxes), nomQcm = nomQcm)
            # Rendu du template 'affichage.html' avec la variable question contenant la liste des questions cochées

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)