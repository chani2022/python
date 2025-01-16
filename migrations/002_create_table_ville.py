"""Peewee migrations -- 002_create_table_ville.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['table_name']            # Return model in current state by name
    > Model = migrator.ModelClass                   # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.run(func, *args, **kwargs)           # Run python function with the given args
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.add_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)
    > migrator.add_constraint(model, name, sql)
    > migrator.drop_index(model, *col_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.drop_constraints(model, *constraints)

"""

from contextlib import suppress

import peewee as pw
from peewee_migrate import Migrator


with suppress(ImportError):
    import playhouse.postgres_ext as pw_pext


def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your migrations here."""
    
    @migrator.create_model
    class Ville(pw.Model):
        id = pw.AutoField()
        ville = pw.CharField(default='NULL', max_length=255)
        code_commune = pw.CharField(default='NULL', max_length=255)
        region = pw.CharField(default='NULL', max_length=255)
        departement = pw.CharField(default='NULL', max_length=255)

        class Meta:
            table_name = "ville"

    # migrator.remove_model('cdc')

    # migrator.remove_model('typechamps')

    # migrator.remove_model('registre')

    # migrator.remove_model('champs')

    # migrator.remove_model('roles')

    # migrator.remove_model('user')

    # migrator.remove_model('production')


def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your rollback migrations here."""
    
    # @migrator.create_model
    # class Production(pw.Model):
    #     id = pw.AutoField()
    #     valeur_champ = pw.CharField(default='NULL', max_length=255)
    #     date_traitement = pw.DateTimeField(default='NULL')
    #     nom_image = pw.CharField(default='NULL', max_length=255)
    #     annee_registre = pw.CharField(default='NULL', max_length=255)
    #     numero_acte = pw.CharField(default='NULL', max_length=255)
    #     user = pw.ForeignKeyField(column_name='user_id', default='NULL', field='id', model=migrator.orm['user'])
    #     cdc = pw.ForeignKeyField(column_name='cdc_id', default='NULL', field='id', model=migrator.orm['cdc'])
    #     registre = pw.ForeignKeyField(column_name='registre_id', default='NULL', field='id', model=migrator.orm['registre'])
    #     champs = pw.ForeignKeyField(column_name='champs_id', default='NULL', field='id', model=migrator.orm['champs'], null=True)

    #     class Meta:
    #         table_name = "production"

    # @migrator.create_model
    # class User(pw.Model):
    #     id = pw.AutoField()
    #     nom = pw.CharField(default='NULL', max_length=255)
    #     prenom = pw.CharField(default='NULL', max_length=255)
    #     matricule = pw.IntegerField(default='NULL', unique=True)
    #     password = pw.CharField(default='NULL', max_length=255)
    #     roles = pw.ForeignKeyField(column_name='roles_id', default='NULL', field='id', model=migrator.orm['roles'])

    #     class Meta:
    #         table_name = "user"

    # @migrator.create_model
    # class Roles(pw.Model):
    #     id = pw.AutoField()
    #     type = pw.CharField(default='NULL', max_length=255)

    #     class Meta:
    #         table_name = "roles"

    # @migrator.create_model
    # class Champs(pw.Model):
    #     id = pw.AutoField()
    #     label_champ = pw.CharField(default='NULL', max_length=255)
    #     name_champs = pw.CharField(default='NULL', max_length=255)
    #     obligatoire = pw.BooleanField(default=True)
    #     position = pw.IntegerField(default='NULL')
    #     typeChamps = pw.ForeignKeyField(column_name='typeChamps_id', default='NULL', field='id', model=migrator.orm['typechamps'])
    #     registre = pw.ForeignKeyField(column_name='registre_id', default='NULL', field='id', model=migrator.orm['registre'])

    #     class Meta:
    #         table_name = "champs"

    # @migrator.create_model
    # class Registre(pw.Model):
    #     id = pw.AutoField()
    #     type_registre = pw.CharField(default='NULL', max_length=255)
    #     cdc = pw.ForeignKeyField(column_name='cdc_id', default='NULL', field='id', model=migrator.orm['cdc'])

    #     class Meta:
    #         table_name = "registre"

    # @migrator.create_model
    # class TypeChamps(pw.Model):
    #     id = pw.AutoField()
    #     type_champs = pw.CharField(default='NULL', max_length=255)

    #     class Meta:
    #         table_name = "typechamps"

    # @migrator.create_model
    # class Cdc(pw.Model):
    #     id = pw.AutoField()
    #     nom_cdc = pw.CharField(default='NULL', max_length=255)

    #     class Meta:
    #         table_name = "cdc"

    migrator.remove_model('ville')
