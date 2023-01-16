from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projet.db'
db.init_app(app)
nombreIdQuestion=0

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

# questions=[]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/visual", methods=['POST','GET'])
def visual():
    if request.method == 'POST':
        question = request.form['question']
        #reponses=[]
        #reponses.append(request.form['nouveauBouton']) , reps = reponses
        return render_template("visualisation.html", question = question)
    else:
        return render_template("ajoutQuestion.html")


@app.route("/ajout",methods = ['POST', 'GET'])
def ajout():
    if request.method == 'POST':
        question = request.form['question']
        new_question = Question(enonce=question)

        try:
            db.session.add(new_question)
            db.session.commit()
            return redirect('/lquestion')
        except:
            return 'erreur'
    else:
        return render_template("ajoutQuestion.html")

@app.route("/plusDeReponse",methods = ['GET'])
def plusDeReponse():
    global nombreIdQuestion
    nombreIdQuestion+=1
    return render_template('partials/nouvelleReponse.html',IdBouton=nombreIdQuestion)

@app.route("/supprimer_bouton", methods=['DELETE'])
def supprimer_bouton():
    id = request.json['id']
    #les questions ne sont pas encore stocké dans une variables donc ne peuvent pas être delete 
    # cursor = connection.cursor()
    # cursor.execute("DELETE FROM boutons WHERE id=%s", (id,))
    # connection.commit()
    # cursor.close()
    #qqc comme ça en bdd
    return jsonify(status='success')

@app.route("/lquestion",methods = ['GET'])
def lquestion():
    questions = db.session.query(Question).all()
    return render_template("lquestion.html",lquestion=questions)

@app.route("/supprimer/<int:id>")
def supprimer(id):
    questionSupp = Question.query.get_or_404(id)

    try:
        db.session.delete(questionSupp)
        db.session.commit()
        return redirect('lquestion')
    except:
        return 'Erreur lors de la suppression de la question'

@app.route("/QCM")
def qcm():
    return render_template("QCM.html")

@app.route("/MesQCM")
def Mesqcm():
    return render_template("/MesQCM.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)