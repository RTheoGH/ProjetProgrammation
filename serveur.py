from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projet.db'
db.init_app(app)
nombreIdQuestion=0
nombreIdCheck=0

# Voir README pour le schèma de la base de données
class Question(db.Model):
    idQ = db.Column(db.Integer, primary_key=True)
    enonce = db.Column(db.String(300), nullable=False)

    def __constructeur__(u):
        return 'Question %r'% u.idQ

class Etiquette(db.Model):
    idE = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))

class Associe(db.Model):
    RidE = db.Column(db.Integer, db.ForeingKey(Etiquette.idE),nullable=False,primary_key=True)
    RidQCM = db.Column(db.Integer, db.ForeingKey(Question.idQ),nullable=False,primary_key=True)

class Reponse(db.Model):
    idR = db.Column(db.Integer,primary_key=True)
    reponse = db.Column(db.String(200), nullable=False)
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
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html",page="Menu")    #Rendu template index.html et parametre nav 

# @app.route("/accueil",methods=['GET'])
# def accueil():
#     utiCO=db.session.query(Utilisateur)
#     return render_template("accueil.html",accueil=utiCO)

@app.route("/ajout",methods = ['POST', 'GET'])
def ajout():
    if request.method == 'POST':
        question = request.form['question']             #Recup question du formulaire
        new_question = Question(enonce=question)        #Création nouvelle question avec enoncé correspondant

        try:
            db.session.add(new_question)                #Ajout question -> base de donnée
            db.session.commit()                         #Envoie des changements
            return redirect(url_for('lquestion'))       #Redirection vers la liste des questions
        except:
            return 'Erreur création de la question'
    else:                                            
        return render_template("ajoutQuestion.html",page="Créer")
    #Rendu template ajoutQuestion.html et parametre nav 

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
    questions = db.session.query(Question).all()        #Récupération questions de la base de données
    return render_template("lquestion.html",lquestion=questions,page="Consulter")
    #Rendu template lquestion.html, questions récupérées, parametre nav

@app.route("/modifier/<int:id>",methods=['POST','GET'])
def modifier(id):
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
    questionSupp = Question.query.get_or_404(id)        #Récupération question correspondant id, sinon erreur

    try:
        db.session.delete(questionSupp)                 #Suppression question de la base de données
        db.session.commit()                             #Envoi des modifications à la base de données
        return redirect(url_for('lquestion'))           #Redirection vers la page de liste des questions
    except:
        return 'Erreur lors de la suppression de la question'
        #Renvoi message d'erreur si échec de la suppression de la question

@app.route("/QCM")
def qcm():
    LQ = db.session.query(Question).all()               #Récupération questions de la base de données
    print(LQ)
    return render_template("QCM.html",ListesQuestions=LQ,page="CréerQcm")
    #Rendu template QCM.html, variables ListesQuestions,parametre nav

@app.route("/MesQCM")
def Mesqcm():
    return render_template("/MesQCM.html",page="ConsulterQcm") #Rendu template MesQCM.html, parametre nav

@app.route("/generate",methods = ['POST'])
def generate():
    print(request.form.items)
    checked_checkboxes = [] 
    reponse_checkboxes = []                            #Initialisation liste pour stocker les questions cochées
    for key, value in request.form.items():
        if value == 'on':
            # checked_checkboxes.append(key)
            # Récupération de l'enoncé de la question correspondant à l'id reçu
            EL = db.session.query(Question).filter(Question.idQ == key).first()
            # Ajout de l'enoncé à la liste des questions cochées
            checked_checkboxes.append(EL)
            ListeReponse = db.session.query(Reponse.reponse).filter(Reponse.idQ==key).all()
            reponse_checkboxes.append(ListeReponse)
    return render_template("affichage.html", listereponse = ListeReponse, listequestion=checked_checkboxes)
            # Rendu du template 'affichage.html' avec la variable question contenant la liste des questions cochées
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)