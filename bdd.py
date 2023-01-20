from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

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