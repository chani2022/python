from peewee import *
from src.Model.PeeweeSqliteDB import db
from src.Model.Cdc import Cdc

class Famille(Model):
    nom_famille = CharField(default='NULL')
    cdc = ForeignKeyField(model=Cdc, backref='cdcs',default='NULL')

    class Meta:
        database = db