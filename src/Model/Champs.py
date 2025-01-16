from peewee import *
from src.Model.PeeweeSqliteDB import db
from src.Model.TypeChamps import TypeChamps
from src.Model.Registre import Registre

class Champs(Model):
    label_champ = CharField(default='NULL')
    name_champs = CharField(default='NULL')
    obligatoire = BooleanField(default='NULL')
    position = IntegerField(default='NULL')
    typeChamps = ForeignKeyField(model=TypeChamps, backref='typeChamps',default='NULL')
    registre = ForeignKeyField(model=Registre, backref='registres', default='NULL')

    class Meta:
        database = db

    # class Meta:
    #     database = db # This model uses the "people.db" database.

