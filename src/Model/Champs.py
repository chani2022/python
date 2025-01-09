from peewee import *
from src.Model.PeeweeSqliteDB import db
from src.Model.TypeChamps import TypeChamps
from src.Model.Registre import Registre

class Champs(Model):
    label_champ = CharField()
    obligatoire = BooleanField()
    position = IntegerField()
    typeChamps = ForeignKeyField(model=TypeChamps, backref='typeChamps')
    registre = ForeignKeyField(model=Registre, backref='registres')

    class Meta:
        database = db

    # class Meta:
    #     database = db # This model uses the "people.db" database.

