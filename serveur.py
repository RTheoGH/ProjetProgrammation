from flask import Flask, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# db = SQLAlchemy(app)

# class baseQ(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     question = db.Column(db.String(300), nullable=False)
#     reponses = db.Column(db.String(200), nullable=False)

#     def __repr__(self):
#         return '<Question %r' % self.id


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