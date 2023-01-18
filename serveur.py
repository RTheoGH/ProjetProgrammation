from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projet.db'
db.init_app(app)
nombreIdQuestion=0
nombreIdCheck=0

class Question(db.Model):
    idQ = db.Column(db.Integer, primary_key=True)
    enonce = db.Column(db.String(300), nullable=False)

    def __constructeur__(u):
        return 'Question %r'% u.idQ

class Reponse(db.Model):
    idR = db.Column(db.Integer,primary_key=True)
    reponse = db.Column(db.String(200), nullable=False)
    idQ = db.Column(db.Integer, db.ForeignKey(Question.idQ),nullable=False)

    def __constructeur__(u):
        return 'Reponse %r'% u.idR

class QCM(db.Model):
    idE = db.Column(db.Integer,primary_key=True)
    Nom = db.Column(db.String(200), nullable = False)

class Contient(db.Model):
    RidE = db.Column(db.Integer, db.ForeignKey(QCM.idE),nullable=False,primary_key=True)
    RidQ = db.Column(db.Integer,db.ForeignKey(Question.idQ),nullable=False,primary_key=True)


with app.app_context():
    db.create_all()
    # db.session.add(Question(enonce="test"))


@app.route("/")
def index():
    return render_template("index.html",page="Menu")

# @app.route("/accueil",methods=['GET'])
# def accueil():
#     utiCO=db.session.query(Utilisateur)
#     return render_template("accueil.html",accueil=utiCO)

@app.route("/ajout",methods = ['POST', 'GET'])
def ajout():
    if request.method == 'POST':
        question = request.form['question']
        new_question = Question(enonce=question)

        try:
            db.session.add(new_question)
            db.session.commit()
            return redirect(url_for('lquestion'))
        except:
            return 'Erreur création de la question'
    else:
        return render_template("ajoutQuestion.html",page="Créer")

@app.route("/plusDeReponse",methods = ['GET'])
def plusDeReponse():
    global nombreIdQuestion,nombreIdCheck
    nombreIdQuestion+=1
    nombreIdCheck+=1
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
    questions = db.session.query(Question).all()
    return render_template("lquestion.html",lquestion=questions,page="Consulter")

@app.route("/modifier/<int:id>",methods=['POST','GET'])
def modifier(id):
    questionModif = Question.query.get_or_404(id)
    if request.method == 'POST':
        questionModif.enonce = request.form['question']

        try:
            db.session.commit()
            return redirect(url_for('lquestion'))
        except:
            return 'Erreur de modification'
    else:
        return render_template("modifQuestion.html",enonce=questionModif.enonce,idQ=questionModif.idQ)


@app.route("/supprimer/<int:id>")
def supprimer(id):
    questionSupp = Question.query.get_or_404(id)
    print(questionSupp)
    try:
        db.session.delete(questionSupp)
        db.session.commit()
        return redirect(url_for('lquestion'))
    except:
        return 'Erreur lors de la suppression de la question'

@app.route("/QCM")
def qcm():
    LQ = db.session.query(Question).all()
    print(LQ)
    return render_template("QCM.html",ListesQuestions=LQ,page="CréerQcm")
@app.route("/MesQCM")
def Mesqcm():
    return render_template("/MesQCM.html",page="ConsulterQcm")

@app.route("/generate",methods = ['POST'])
def generate():
    print(request.form.items)
    checked_checkboxes = []
    reponse_checkboxes = []
    for key, value in request.form.items():
        if value == 'on':
            # checked_checkboxes.append(key)
            EL = db.session.query(Question.enonce).filter(Question.idQ == key).first()
            checked_checkboxes.append(EL[0])
            ListeReponse = db.session.query(Reponse.reponse).filter(Reponse.idQ==key).all()
            reponse_checkboxes.append(ListeReponse)
            print(ListeReponse)

    return render_template("affichage.html",reponse = ListeReponse, question=checked_checkboxes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)