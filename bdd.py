from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Voir README pour le schéma de la base de données

class Utilisateur(db.Model):                             # Classe Utilisateur
    idU = db.Column(db.Integer, primary_key=True)        #   identifiant de l'utilisateur
    nomU = db.Column(db.String(50))                      #   nom de l'utilisateur
    passU = db.Column(db.String(50))                     #   mot de passe de l'utilisateur

    def __repr__(u):                                     # représentation de l'objet 
        return 'Utilisateur %r'% u.idU                   # pour un print par exemple

class Etudiant(db.Model):                                # Classe Etudiant
    numeroEtu = db.Column(db.Integer, primary_key=True)  #   identifiant de l'étudiant (son numero d'étudiant)
    nomEtu = db.Column(db.String(50))                    #   nom de l'étudiant
    prenomEtu = db.Column(db.String(50))                 #   prenom de l'étudiant
    mdpEtu = db.Column(db.String(50))                    #   mot de passe de l'étudiant

    def __repr__(u):
        return 'Etudiant : %r' % u.numeroEtu

class Classe(db.Model):
    idCU = db.Column(db.Integer, db.ForeignKey(Utilisateur.idU),nullable=False,primary_key=True)
    idCE = db.Column(db.Integer, db.ForeignKey(Etudiant.numeroEtu),nullable=False,primary_key=True)

class Question(db.Model):                                                        # Classe Question
    idQ = db.Column(db.String(50), primary_key=True)                             #   identifiant question
    enonce = db.Column(db.String(300), nullable=False)                           #   énoncé question
    idU = db.Column(db.Integer, db.ForeignKey(Utilisateur.idU), nullable=False)  #   id référence de id utilisateur

    def __repr__(u):
        return 'Question %r'% u.idQ

class Etiquette(db.Model):                                                       # Classe Etiquette
    idE = db.Column(db.Integer, primary_key=True)                                #   id etiquette  
    nom = db.Column(db.String(100))                                              #   nom etiquette
    idU = db.Column(db.Integer, db.ForeignKey(Utilisateur.idU), nullable=False)  #   id référence de id utlisateur

    def __repr__(u):
        return 'Etiquette %r'% u.idE

class Associe(db.Model):                                                  # Classe association entre etiquette et question
    RidE = db.Column(db.Integer, db.ForeignKey(Etiquette.idE),nullable=False,primary_key=True) # id référence id etiquette
    RidQ = db.Column(db.String(50), db.ForeignKey(Question.idQ),nullable=False,primary_key=True)  # id référence id question

class Reponse(db.Model):                                                    # Classe Reponse
    idR = db.Column(db.Integer,primary_key=True)                            #   identifiant reponse
    reponse = db.Column(db.String(200), nullable=False)                     #   corps de la reponse
    correction = db.Column(db.Integer, nullable=False)                      #   boolean vrai/faux
    estNumerique = db.Column(db.Boolean,default = False, nullable = False)
    idQ = db.Column(db.String(50), db.ForeignKey(Question.idQ),nullable=False) #   id référence de id question

    def __repr__(u):
        return 'Reponse %r'% u.idR

class QCM(db.Model):                                                             # Classe QCM
    idQCM = db.Column(db.String(50),primary_key=True)                            #   id qcm
    Nom = db.Column(db.String(200), nullable = False)                            #   nom du qcm
    idU = db.Column(db.Integer, db.ForeignKey(Utilisateur.idU), nullable=False)  #   id référence de id utilisateur
    
    def __repr__(u):
        return 'QCM %r'% u.idQCM

class Contient(db.Model):                                                 # Classe association entre qcm et question
    RidQCM = db.Column(db.String(50), db.ForeignKey(QCM.idQCM),nullable=False,primary_key=True) # id référence id qcm
    RidQ = db.Column(db.String(50),db.ForeignKey(Question.idQ),nullable=False,primary_key=True) # id référence id question
    Position = db.Column(db.Integer,default=0, nullable=False)                                  # Position

class ReponseEtudiant(db.Model):
    numeroEtu = db.Column(db.Integer,db.ForeignKey(Etudiant.numeroEtu),primary_key=True)
    idQCM = db.Column(db.String(50),db.ForeignKey(QCM.idQCM),primary_key=True)
    RidQ = db.Column(db.String(50),db.ForeignKey(Question.idQ),nullable=False,primary_key=True)
    date = db.Column(db.String(100),nullable = False)
    estNumerique = db.Column(db.Boolean,default = False, nullable = False)
    Value = db.Column(db.Integer,nullable = False)#si numerique = false alors si value = 0 => false, sinon true

class Test(db.Model):
    numeroEtu = db.Column(db.Integer,db.ForeignKey(Etudiant.numeroEtu),primary_key=True)
    date = db.Column(db.String(100),nullable = False)
    estNumerique = db.Column(db.Boolean,default = False, nullable = False)
    Value = db.Column(db.Integer,nullable = False)