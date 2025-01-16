from peewee import *
from src.Model.PeeweeSqliteDB import db
from src.Model.User import User
from src.Model.Cdc import Cdc
from src.Model.Registre import Registre
from src.Model.Champs import Champs

class Production(Model):
    valeur_champ = CharField(default='NULL')
    date_traitement = DateTimeField(default='NULL')
    nom_image = CharField(default='NULL')
    annee_registre = CharField(default='NULL')
    numero_acte = CharField(default='NULL')

    user = ForeignKeyField(model=User, backref='users', default='NULL')
    cdc = ForeignKeyField(model=Cdc, backref='cdcs', default='NULL')
    registre = ForeignKeyField(model=Registre, backref='registres', default='NULL')
    champs = ForeignKeyField(model=Champs, null= True, backref='champs', default='NULL')


    class Meta:
        database = db