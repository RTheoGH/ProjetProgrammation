from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

questions=[]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ajout",methods = ['POST', 'GET'])
def ajout():
    if request.method == 'POST':
        question = request.form['question']
        questions.append(question)
        return redirect(url_for('lquestion'))
    else:
        return render_template("ajoutQuestion.html")

@app.route("/lquestion",methods = ['GET'])
def lquestion():
    return render_template("lquestion.html",lquestion=questions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)