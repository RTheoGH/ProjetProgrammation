from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ajout",methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        return redirect(url_for('stock'))
    else:
        return render_template("ajout.html")

@app.route("/stock",methods = ['GET'])
def stock():
    return render_template("stock.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)