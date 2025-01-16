from peewee import *
from src.Model.PeeweeSqliteDB import db
from src.Model.Cdc import Cdc

class Registre(Model):
    type_registre = CharField(default='NULL')
    cdc = ForeignKeyField(model=Cdc, backref='cdcs', default='NULL')

    class Meta:
        database = db

    # class Meta:
    #     database = db # This model uses the "people.db" database.

