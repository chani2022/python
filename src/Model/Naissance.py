from peewee import *
from src.Model.PeeweeSqliteDB import db
from src.Model.User import User
from src.Model.Famille import Famille

class Naissance(Model):
    code_commune = CharField()
    code_famille_acte = CharField()
    numero_registre = CharField()
    code_etat = CharField()
    famille = ForeignKeyField(model=Famille, backref='familles')
    date_traitement = DateField(default='NULL')
    heure_traitement = TimeField(default='NULL')
    user = ForeignKeyField(model=User, backref='users')
    nom_fichier = CharField(default='NULL')
    
    
    """
        CE QUI SUIT SONT LES CHAMPS VISIBLE DANS LA SAISIE
    """
    """
        *principal
    """
    nom_principal = CharField() 
    prenom_principal = CharField()
    lieu_naissance_principal = CharField()
    date_naissance_principal = DateField()
    rue_domicile_principal = CharField()
    ville_domicile_principal = CharField(default="NULL")
    """
        *pere
    """
    nom_pere = CharField()
    prenom_pere = CharField()
    lieu_naissance_pere = CharField(default='NULL')
    date_naissance_pere = DateField()
    rue_domicile_pere = CharField(default='NULL')
    ville_domicile_pere = CharField(default="NULL")
    """
        *mere
    """
    nom_mere = CharField(default='NULL')
    prenom_mere = CharField(default='NULL')
    lieu_naissance_mere = CharField(default='NULL')
    date_naissance_mere = DateField()
    rue_domicile_mere = CharField(default='NULL')
    ville_domicile_mere = CharField(default="NULL")

    """
        *autre champs
    """
    numero_acte = CharField()
    code_sexe = CharField()
    date_evenement = DateField()
    lieu_evenement = CharField(default='NULL')
    heure_evenement = TimeField()
    date_dresse = DateField(default='NULL')
    heure_dresse = TimeField(default='NULL')
    type_acte = CharField(default='NULL')
    annotation = CharField(default="NULL")

    class Meta:
        database = db

    # class Meta:
    #     database = db # This model uses the "people.db" database.

