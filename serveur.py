from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import MultiDict, ImmutableMultiDict


db = SQLAlchemy()
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  #Pour la session sinon ça marche pas
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projet.db'
db.init_app(app)
nombreIdQuestion=0
nombreIdCheck=0

# Voir README pour le schèma de la base de données
class Utilisateur(db.Model):
    idU = db.Column(db.Integer, primary_key=True)
    nomU = db.Column(db.String(50))
    passU = db.Column(db.String(50))

    def __constructeur__(u):
        return 'Utilisateur %r'% u.idU

class Question(db.Model):
    idQ = db.Column(db.Integer, primary_key=True)
    enonce = db.Column(db.String(300), nullable=False)
    # idU = db.Column(db.Integer, db.ForeignKey(Utilisateur.idU), nullable=False)

    def __constructeur__(u):
        return 'Question %r'% u.idQ

class Etiquette(db.Model):
    idE = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))

class Associe(db.Model):
    RidE = db.Column(db.Integer, db.ForeignKey(Etiquette.idE),nullable=False,primary_key=True)
    RidQ = db.Column(db.Integer, db.ForeignKey(Question.idQ),nullable=False,primary_key=True)

class Reponse(db.Model): 
    idR = db.Column(db.Integer,primary_key=True)
    reponse = db.Column(db.String(200), nullable=False)
    correction = db.Column(db.Integer, nullable=False)
    idQ = db.Column(db.Integer, db.ForeignKey(Question.idQ),nullable=False)

    def __constructeur__(u):
        return 'Reponse %r'% u.idR

class QCM(db.Model):
    idQCM = db.Column(db.Integer,primary_key=True)
    Nom = db.Column(db.String(200), nullable = False)

class Contient(db.Model):
    RidQCM = db.Column(db.Integer, db.ForeignKey(QCM.idQCM),nullable=False,primary_key=True)
    RidQ = db.Column(db.Integer,db.ForeignKey(Question.idQ),nullable=False,primary_key=True)

with app.app_context():
    #db.drop_all()
    db.create_all()
    
with app.app_context():
    db.session.query(Associe).delete()
    db.session.commit()
    db.session.query(Etiquette).delete()
    db.session.commit()
    db.session.query(Question).delete()
    db.session.commit()
    db.session.query(Question).delete()
    db.session.commit()
    etiquettes = [Etiquette(nom='Calcul'), Etiquette(nom='Equation'), Etiquette(nom='Code')]
    db.session.bulk_save_objects(etiquettes)
    db.session.commit()
    questions = [Question(enonce='2+2'),Question(enonce='2*2'),Question(enonce='2/2')]
    db.session.bulk_save_objects(questions)
    db.session.commit()
    assos = [Associe(RidE=1,RidQ=1),Associe(RidE=1,RidQ=2),Associe(RidE=2,RidQ=3),Associe(RidE=3,RidQ=1)] 
    db.session.bulk_save_objects(assos)
    db.session.commit()

@app.route("/")
def index():
    return render_template("index.html",page="Menu")    #Rendu template index.html et parametre nav 

@app.route("/creationCompte",methods = ['POST', 'GET'])
def creationCompte():
    if request.method == 'POST':
        nomUtilisateur = request.form['creationNom']
        mdpUtilisateur = request.form['creationMdp']
        new_utilisateur = Utilisateur(nomU=nomUtilisateur,passU=mdpUtilisateur)
        print(nomUtilisateur)
        print(mdpUtilisateur)
        print(new_utilisateur)
        try:
            db.session.add(new_utilisateur)
            db.session.commit()
            return redirect(url_for("index"))
        except:
            return 'Erreur lors de la création du compte'
    else: 
        return render_template("creationCompte.html")

@app.route("/listeUtilisateurs",methods = ['GET'])        #Cette route est uniquement technique pour pouvoir
def listeUtilisateurs():                                  #visualiser les utilisateurs en aucun cas elle doit
    if 'nomU' not in session or session['nomU']!='ADMIN': #etre accessible via une redirection ou autre
        flash("Vous n'avez pas les droits pour accéder à cette page")
        return redirect(url_for('index'))
    utilisateurs = db.session.query(Utilisateur).all()  
    return render_template("lUtilisateurs.html",lUtilisateurs=utilisateurs,page='listeUtilisateurs')

@app.route("/connexion",methods=['POST','GET'])
def connexion():
    if request.method == 'POST':
        testLogin = db.session.query(Utilisateur).filter(Utilisateur.nomU == request.form['nomU']).first()
        # if request.form['nomU'] == request.form['passU']:
        if testLogin is None:
            flash('Nom ou mot de passe invalide')
            return redirect(url_for('connexion'))
        if request.form['passU'] == testLogin.passU:
            session['nomU'] = request.form['nomU']
        return redirect(url_for("index"))
    else:                       
        return render_template("connexion.html")

@app.route("/deconnexion")
def deconnexion():
    session.pop('nomU',None)
    return redirect(url_for("index"))

@app.route("/ajout",methods = ['POST', 'GET'])
def ajout():
    if 'nomU' not in session:
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    if request.method == 'POST':
        question = request.form['question']             #Recup question du formulaire
        new_question = Question(enonce=question)        #Création nouvelle question avec enoncé correspondant
        recupForm = request.form.getlist("reponse")
        
        try:
        
            db.session.add(new_question)                #Ajout question -> base de donnée
            db.session.commit()                         #Envoie des changements
            listeOn = []                              
            for key,value in request.form.items():
                if value == 'on':
                    listeOn.append(int(key))
            idQuestion = db.session.query(Question.idQ).filter(Question.enonce == question).first()
            for rep in recupForm:
                
                reponseAjouter = 0
                if (recupForm.index(rep)+1) in listeOn:
                    reponseAjouter = Reponse(reponse= rep,correction = 1,idQ =idQuestion[0])
                    db.session.add(reponseAjouter)
                else:
                    reponseAjouter = Reponse(reponse= rep,correction = 0,idQ =idQuestion[0])
                    db.session.add(reponseAjouter)       
            db.session.commit()
            
            selected_tags = request.form.getlist('tag')
            for tag_id in selected_tags:
                # tag = db.session.query(Etiquette).filter(Etiquette.idE == tag_id).first()
                # print(tag_id,new_question.idQ)
                new_assos = Associe(RidE=tag_id,RidQ=new_question.idQ)
                # print(new_assos.RidE,new_assos.RidQ)
                db.session.add(new_assos)
                # print(new_assos,"add ?")
                db.session.commit()
                # print("encore vivant")
            # test=Associe.query.all()
            # print(test)
        # db.session.commit()                         #Envoie des changements
            return redirect(url_for('lquestion'))       #Redirection vers la liste des questions
        except:
            return 'Erreur création de la question'
    else:                                            
        return render_template("ajoutQuestion.html",page="Créer")
    #Rendu template ajoutQuestion.html et parametre nav 

@app.route("/creationEtiquettes",methods=['GET','POST'])
def creationEtiquettes():
    if 'nomU' not in session:
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    if request.method == 'POST':
        nom = request.form['nom']
        new_etiquette = Etiquette(nom=nom)
        try :
            db.session.add(new_etiquette)
            db.session.commit()
            print(Etiquette.query.all(),new_etiquette.nom,new_etiquette.idE)
            return redirect(url_for('index'))
        except:
            return 'Erreur : route /creationEtiquettes'
    else :
        return render_template("creationEtiquettes.html",page="CreationEtiquettes")

@app.route("/suppEtiquettes",methods=['GET','POST'])
def suppEtiquettes():
    if 'nomU' not in session:
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    print('avant suppression : ',Etiquette.query.all())
    if request.method == 'POST':
        nom = request.form['nom']
        print(nom)
        try :
            test = db.session.query(Associe).join(Etiquette,Associe.RidE == Etiquette.idE).filter(Etiquette.nom == nom).all()
            etiq = db.session.query(Etiquette).filter(Etiquette.nom==nom).first()
            print('assos : ',assos,' tout :', db.session.query(Associe).all(), 'test join : ', test) 
            for associe in test:
                print('associe : ',associe)
                db.session.delete(associe)
                db.session.commit()
            else:
                print("Etiquette not found")
            print('après suppression : ',Etiquette.query.all(),' association : ',Associe.query.all())
            db.session.delete(etiq)
            db.session.commit()
            return redirect(url_for('creationEtiquettes'))
        except:
            return 'Erreur : route /suppEtiquettes'
    else :
        return render_template("creationEtiquettes.html")

@app.route("/creerQuestion",methods=['GET','POST'])
def creerQ():
    if 'nomU' not in session:
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    etiquettes = Etiquette.query.all()
    return render_template('ajoutQuestion.html', etiquettes=etiquettes, page="Créer")

@app.route("/plusDeReponse",methods = ['GET'])
def plusDeReponse():
    global nombreIdQuestion,nombreIdCheck               #Déclaration variables globales nombreIdQuestion, nombreIdCheck
    nombreIdQuestion+=1                                 #Incrémentation de nombreIdQuestion et nombreIdCheck
    nombreIdCheck+=1                                    #de 1 (pour avoir des id différent pour chaque objet)
    return render_template('partials/nouvelleReponse.html',IdBouton=nombreIdQuestion,IdCheck=nombreIdCheck)
    # Rendu template 'partials/nouvelleReponse.html' et passage des paramètres IdBouton et IdCheck

@app.route("/supprimer_bouton", methods=['DELETE'])
def supprimer_bouton():
    id = request.json['id']
    #les questions ne sont pas encore stocké dans une variables donc ne peuvent pas être delete 
    # cursor = connection.cursor()
    # cursor.execute("DELETE FROM boutons WHERE id=%s", (id,))
    # connection.commit()
    # cursor.close()
    #qqc comme ça en bdd
    return 'SUCCES'

@app.route("/lquestion",methods = ['GET'])
def lquestion():
    if 'nomU' not in session:
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    questions = db.session.query(Question).all()
    # tag = db.session.query(Etiquette, Associe).join(Associe, Etiquette.idE == Associe.RidE).join(Question, Question.idQ == Associe.RidQ).all()
    # print(tag)
    return render_template("lquestion.html",lquestion=questions,page="Consulter")
    #Rendu template lquestion.html, questions récupérées, parametre nav

@app.route("/modifier/<int:id>",methods=['POST','GET'])
def modifier(id):
    if 'nomU' not in session:
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    questionModif = Question.query.get_or_404(id)       #Recup question avec id correspondant, erreur sinon
    if request.method == 'POST':
        questionModif.enonce = request.form['question'] #Modification de l'enoncé de la question
        try:
            db.session.commit()                         #Envoi des modifications à la base de données
            return redirect(url_for('lquestion'))       #Redirection vers la page de liste des questions
        except:
            return 'Erreur de modification'             #Renvoi message erreur en cas d'échec de la modification
    else:
        return render_template("modifQuestion.html",enonce=questionModif.enonce,idQ=questionModif.idQ)
        #Rendu template modifQuestion.html avec les variables enonce et idQ

@app.route("/supprimer/<int:id>")
def supprimer(id):
    if 'nomU' not in session:
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    questionSupp = Question.query.get_or_404(id)        #Récupération question correspondant id, sinon erreur
    toutAssocie = db.session.query(Associe).all()    
    reponseSupp = db.session.query(Reponse.idR).filter(Reponse.idQ==id).all()
    try:
        for key in reponseSupp:
            Asupp = Reponse.query.get_or_404(key)
            db.session.delete(Asupp)
        for assoc in toutAssocie :
            if(assoc.RidQ==id):
                db.session.delete(assoc)
                db.session.commit()
        db.session.delete(questionSupp)                 #Suppression question de la base de données
        db.session.commit()                             #Envoi des modifications à la base de données
        return redirect(url_for('lquestion'))           #Redirection vers la page de liste des questions
    except:
        return 'Erreur lors de la suppression de la question'
        #Renvoi message d'erreur si échec de la suppression de la question

@app.route("/QCM")
def qcm():
    if 'nomU' not in session:
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    LQ = db.session.query(Question).all()               #Récupération questions de la base de données
    print(LQ)
    return render_template("QCM.html",ListesQuestions=LQ,page="CréerQcm")
    #Rendu template QCM.html, variables ListesQuestions,parametre nav

@app.route("/MesQCM")
def Mesqcm():
    if 'nomU' not in session:
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    return render_template("/MesQCM.html",page="ConsulterQcm") #Rendu template MesQCM.html, parametre nav

@app.route("/generate",methods = ['POST'])
def generate():
    if 'nomU' not in session:
        flash("Connectez vous ou créer un compte pour accéder à cette page")
        return redirect(url_for('index'))
    print(request.form.items)
    print(db.session.query(Reponse.idR).all())
    print(db.session.query(Reponse.reponse).all())
    print(db.session.query(Reponse.idQ).all())
    checked_checkboxes = [] 
    reponse_checkboxes = []                         #Initialisation liste pour stocker les questions cochées
    nomQcm =request.form['nomQcm']
    #insert sur qcm avec un idqcm : 
    #db.session.add(QCM(Nom = ))
    for key, value in request.form.items():
        if value == 'on':
            # checked_checkboxes.append(key)
            # Récupération de l'enoncé de la question correspondant à l'id reçu
            EL = db.session.query(Question).filter(Question.idQ == key).first()
            checked_checkboxes.append(EL)
            #insert to dans contient idqcm(global a cette fun) et EL.idQ 
            # Ajout de l'enoncé à la liste des questions cochées
            ListeReponse = db.session.query(Reponse).filter(Reponse.idQ==key).all()
            reponse_checkboxes.append(ListeReponse)
    return render_template("Affichage.html", listereponse = reponse_checkboxes, listequestion=checked_checkboxes,len = len(checked_checkboxes), nomQcm = nomQcm)
            # Rendu du template 'affichage.html' avec la variable question contenant la liste des questions cochées
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)