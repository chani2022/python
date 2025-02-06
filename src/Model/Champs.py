from peewee import *
from src.Model.PeeweeSqliteDB import db
from src.Model.Famille import Famille

class Champs(Model):
    label_champ = CharField(default='NULL')
    name_champs = CharField(default='NULL')
    obligatoire = BooleanField(default='NULL')
    position = IntegerField(default='NULL')
    famille = ForeignKeyField(model=Famille, backref='typeActes', default='NULL')

    class Meta:
        database = db

    # class Meta:
    #     database = db # This model uses the "people.db" database.

