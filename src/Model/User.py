from peewee import *
from src.Model.PeeweeSqliteDB import db
from src.Model.RolesUser import Roles

class User(Model):
    nom = CharField(default='NULL')
    prenom = CharField(default='NULL')
    matricule = IntegerField(unique=True,default='NULL')
    password = CharField(default='NULL')
    roles = ForeignKeyField(model=Roles, backref='users', default='NULL')

    class Meta:
        database = db

    # class Meta:
    #     database = db # This model uses the "people.db" database.

