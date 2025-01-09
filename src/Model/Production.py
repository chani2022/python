from peewee import *
from src.Model.PeeweeSqliteDB import db
from src.Model.User import User
from src.Model.Cdc import Cdc
from src.Model.Registre import Registre
from src.Model.Champs import Champs

class Production(Model):
    valeur_champ = CharField()
    date_traitement = DateTimeField()
    nom_image = CharField()

    typeChamps = ForeignKeyField(model=User, backref='users')
    cdc = ForeignKeyField(model=Cdc, backref='cdcs')
    registre = ForeignKeyField(model=Registre, backref='registres')
    champs = ForeignKeyField(model=Champs, backref='champs')

    class Meta:
        database = db