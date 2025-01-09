"""Peewee migrations -- 007_create_production_table.py.

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
    class Production(pw.Model):
        id = pw.AutoField()
        valeur_champ = pw.CharField(max_length=255)
        date_traitement = pw.DateTimeField()
        nom_image = pw.CharField(max_length=255)
        typeChamps = pw.ForeignKeyField(column_name='typeChamps_id', field='id', model=migrator.orm['user'])
        cdc = pw.ForeignKeyField(column_name='cdc_id', field='id', model=migrator.orm['cdc'])
        registre = pw.ForeignKeyField(column_name='registre_id', field='id', model=migrator.orm['registre'])
        champs = pw.ForeignKeyField(column_name='champs_id', field='id', model=migrator.orm['champs'])

        class Meta:
            table_name = "production"

    # migrator.remove_model('typechamps')

    # migrator.remove_model('roles')


def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your rollback migrations here."""
    
    # @migrator.create_model
    # class Roles(pw.Model):
    #     id = pw.AutoField()
    #     type = pw.CharField(max_length=255)

    #     class Meta:
    #         table_name = "roles"

    # @migrator.create_model
    # class TypeChamps(pw.Model):
    #     id = pw.AutoField()
    #     type_champs = pw.CharField(max_length=255)

    #     class Meta:
    #         table_name = "typechamps"

    migrator.remove_model('production')
