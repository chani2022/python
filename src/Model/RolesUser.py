from peewee import *
from src.Model.PeeweeSqliteDB import db


class Roles(Model):
    type = CharField()

    class Meta:
        database = db