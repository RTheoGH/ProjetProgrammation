from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projet.db'
db.init_app(app)

class Question(db.Model):
    idQ = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(300), nullable=False)
    reponses = db.Column(db.String(200),db.ForeignKey('reponse.idR'), nullable=False)

    def __constructeur(u):
        return 'Question %r'% u.idQ

class Reponse(db.Model):
    idR = db.Column(db.Integer,primary_key=True)
    reponse = db.Column(db.String(200), nullable=False)

    def __constructeur(u):
        return 'Reponse %r'% u.idR

with app.app_context():
    db.create_all()

questions=[]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ajout",methods = ['POST', 'GET'])
def ajout():
    if request.method == 'POST':
        question = request.form['question']
        reponse = request.form['reponse']
        questions.append({"question":question,"reponse":reponse})
        return redirect(url_for('lquestion'))
    else:
        return render_template("ajoutQuestion.html")

@app.route("/lquestion",methods = ['GET'])
def lquestion():
    return render_template("lquestion.html",lquestion=questions)

@app.route("/supprimer")
def modifier():
    questions.remove()
    return redirect(url_for("lquestion"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)