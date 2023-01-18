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
    # db.session.add(Question(enonce="test"))


@app.route("/")
def index():
        # Rendu du template 'index.html' et passage du paramètre page 
    return render_template("index.html",page="Menu")

# @app.route("/accueil",methods=['GET'])
# def accueil():
#     utiCO=db.session.query(Utilisateur)
#     return render_template("accueil.html",accueil=utiCO)

@app.route("/ajout",methods = ['POST', 'GET'])
def ajout():
    if request.method == 'POST':
        # Récupération de la question depuis le formulaire
        question = request.form['question']
        # Création d'un nouvel objet Question avec l'enoncé de la question
        new_question = Question(enonce=question)
        try:
            # Ajout de la nouvelle question à la session de la base de données
            db.session.add(new_question)
            # Envoi des changements à la base de données
            db.session.commit()
            # Redirection vers la page de liste des questions
            return redirect(url_for('lquestion'))
        except: # Renvoi d'un message d'erreur en cas d'échec de la création de la question
            return 'Erreur création de la question'
    else: # Si la méthode de la requête est 'GET', rendu du template 'ajoutQuestion.html' avec la page 'Créer'
        return render_template("ajoutQuestion.html",page="Créer")

@app.route("/plusDeReponse",methods = ['GET'])
def plusDeReponse():
    # Déclaration des variables globales nombreIdQuestion, nombreIdCheck
    global nombreIdQuestion,nombreIdCheck
    # Incrémentation de nombreIdQuestion et nombreIdCheck de 1 ( pour avoir des id différent pour chaque objet )
    nombreIdQuestion+=1
    nombreIdCheck+=1
    # Rendu du template 'partials/nouvelleReponse.html' et passage des paramètres IdBouton et IdCheck
    return render_template('partials/nouvelleReponse.html',IdBouton=nombreIdQuestion,IdCheck=nombreIdCheck)

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
    # Récupération de toutes les questions de la base de données
    questions = db.session.query(Question).all()
    # Rendu du template 'lquestion.html' avec les questions récupérées et la variable page = 'Consulter'
    return render_template("lquestion.html",lquestion=questions,page="Consulter")

@app.route("/modifier/<int:id>",methods=['POST','GET'])
def modifier(id):
    # Récupération de la question correspondant à l'id spécifié, ou renvoi d'une erreur 404 si elle n'existe pas
    questionModif = Question.query.get_or_404(id)
    if request.method == 'POST':
        # Modification de l'enoncé de la question
        questionModif.enonce = request.form['question']
        try:
            # Envoi des modifications à la base de données
            db.session.commit()
            # Redirection vers la page de liste des questions
            return redirect(url_for('lquestion'))
        except:
            # Renvoi d'un message d'erreur en cas d'échec de la modification
            return 'Erreur de modification'
    else:
        # Si la méthode de la requête est 'GET', rendu du template 'modifQuestion.html'
        # avec les variables enonce et idQ
        return render_template("modifQuestion.html",enonce=questionModif.enonce,idQ=questionModif.idQ)


@app.route("/supprimer/<int:id>")
def supprimer(id):
    # Récupération de la question correspondant à l'id spécifié, 
    # ou renvoi d'une erreur 404 si elle n'existe pas
    questionSupp = Question.query.get_or_404(id)
    print(questionSupp)
    try:
        # Suppression de la question de la session de la base de données
        db.session.delete(questionSupp)
        # Envoi des modifications à la base de données
        db.session.commit()
        # Redirection vers la page de liste des questions
        return redirect(url_for('lquestion'))
    except:
        # Renvoi d'un message d'erreur en cas d'échec de la suppression de la question
        return 'Erreur lors de la suppression de la question'

@app.route("/QCM")
def qcm():
    # Récupération de toutes les questions de la base de données
    LQ = db.session.query(Question).all()
    print(LQ)
    # Rendu du template 'QCM.html' avec les variables ListesQuestions et la page = 'CréerQcm'
    return render_template("QCM.html",ListesQuestions=LQ,page="CréerQcm")
@app.route("/MesQCM")
def Mesqcm():
    # Rendu du template '/MesQCM.html' avec la variable page = 'ConsulterQcm'
    return render_template("/MesQCM.html",page="ConsulterQcm")

@app.route("/generate",methods = ['POST'])
def generate():
    print(request.form.items)
    # Initialisation d'une liste pour stocker les questions cochées
    checked_checkboxes = []
    for key, value in request.form.items():
        if value == 'on':
            # checked_checkboxes.append(key)
            # Récupération de l'enoncé de la question correspondant à l'id reçu
            EL = db.session.query(Question.enonce).filter(Question.idQ == key).first()
            # Ajout de l'enoncé à la liste des questions cochées
            checked_checkboxes.append(EL[0])
            # Rendu du template 'affichage.html' avec la variable question contenant la liste des questions cochées
    return render_template("affichage.html", question=checked_checkboxes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)