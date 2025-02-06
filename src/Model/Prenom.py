from peewee import *
from src.Model.PeeweeSqliteDB import db

class Prenom(Model):
    prenom = CharField(default="NULL")

    class Meta:
        database = db