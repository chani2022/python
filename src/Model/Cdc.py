from peewee import *
from src.Model.PeeweeSqliteDB import db

class Cdc(Model):
    nom_cdc = CharField(default='NULL')

    class Meta:
        database = db