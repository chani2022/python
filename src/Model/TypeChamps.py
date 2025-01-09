from peewee import *
from src.Model.PeeweeSqliteDB import db

class TypeChamps(Model):
    type_champs = CharField()

    class Meta:
        database = db

    # class Meta:
    #     database = db # This model uses the "people.db" database.

