from peewee import *
from src.Model.PeeweeSqliteDB import db


class Roles(Model):
    type = CharField(default='NULL')

    class Meta:
        database = db