"""Peewee migrations -- 007_add_field_annotation_table_naissance.py.

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
    
    migrator.add_fields(
        'naissance',

        annotation=pw.CharField(default='NULL', max_length=255))

    # migrator.change_fields('naissance', user=pw.ForeignKeyField(column_name='user_id', default='NULL', field='id', model=migrator.orm['user']))

    # migrator.remove_model('cdc')

    # migrator.remove_model('champs')

    # migrator.remove_model('roles')

    # migrator.remove_model('typeacte')

    # migrator.remove_model('ville')


def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your rollback migrations here."""
    
    migrator.remove_fields('naissance', 'annotation')

    # @migrator.create_model
    # class Ville(pw.Model):
    #     id = pw.AutoField()
    #     commune = pw.CharField(max_length=255, null=True)
    #     departement = pw.CharField(max_length=255, null=True)

    #     class Meta:
    #         table_name = "ville"

    # @migrator.create_model
    # class TypeActe(pw.Model):
    #     id = pw.AutoField()
    #     nom_type_acte = pw.CharField(default='NULL', max_length=255)
    #     valeur = pw.CharField(default='NULL', max_length=255)
    #     famille = pw.ForeignKeyField(column_name='famille_id', default='NULL', field='id', model=migrator.orm['famille'])

    #     class Meta:
    #         table_name = "typeacte"

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
    #     famille = pw.ForeignKeyField(column_name='famille_id', default='NULL', field='id', model=migrator.orm['famille'])

    #     class Meta:
    #         table_name = "champs"

    # @migrator.create_model
    # class Cdc(pw.Model):
    #     id = pw.AutoField()
    #     nom_cdc = pw.CharField(default='NULL', max_length=255)

    #     class Meta:
    #         table_name = "cdc"
