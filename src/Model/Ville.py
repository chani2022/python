from peewee import *
from src.Model.PeeweeSqliteDB import db


class Ville(Model):
    ville = CharField(null=True)
    code_commune = CharField(null=True)
    region = CharField(null=True)
    departement = CharField(null=True)

    class Meta:
        database = db

    # class Meta:
    #     database = db # This model uses the "people.db" database.

