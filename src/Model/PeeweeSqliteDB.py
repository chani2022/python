from peewee import SqliteDatabase

db = SqliteDatabase('bdd/masque.db', pragmas={'foreign_keys': 1})

