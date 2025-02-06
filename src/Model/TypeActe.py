from peewee import *
from src.Model.PeeweeSqliteDB import db
from src.Model.Famille import Famille

class TypeActe(Model):
    nom_type_acte = CharField(default='NULL')
    valeur = CharField(default='NULL')
    famille = ForeignKeyField(model=Famille, backref='familles', default='NULL')

    class Meta:
        database = db

    # class Meta:
    #     database = db # This model uses the "people.db" database.

