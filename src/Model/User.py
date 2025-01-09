from peewee import *
from src.Model.PeeweeSqliteDB import db
from src.Model.RolesUser import Roles

class User(Model):
    nom = CharField()
    prenom = CharField()
    matricule = IntegerField(unique=True)
    password = CharField()
    roles = ForeignKeyField(model=Roles, backref='users')

    class Meta:
        database = db

    # class Meta:
    #     database = db # This model uses the "people.db" database.

