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

with app.app_context():
    db.create_all()
    # db.session.add(Question(enonce="test"))

questions=[]
quest=[["faze","a"],["kirito","b"],["guts","c"]]

@app.route("/")
def index():
    return render_template("index.html")

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
        return render_template("ajoutQuestion.html")

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
    return render_template("lquestion.html",lquestion=questions)

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
    return render_template("QCM.html",ListesQuestions=quest)
@app.route("/MesQCM")
def Mesqcm():
    return render_template("/MesQCM.html")

@app.route("/generate")
def generate():
    print(request.args.items)
    checked_checkboxes = []
    print(request.args)
    print(request.args.items)
    for key, value in request.args.items():
        if value == 'on':
            checked_checkboxes.append(key)
    
    return 'Checked checkboxes: {}'.format(checked_checkboxes)
    return render_template("/Affichage.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)