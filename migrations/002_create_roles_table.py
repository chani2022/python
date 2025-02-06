"""Peewee migrations -- 002_create_roles_table.py.

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
    class Roles(pw.Model):
        id = pw.AutoField()
        type = pw.CharField(default='NULL', max_length=255)

        class Meta:
            table_name = "roles"

    # migrator.remove_model('cdc')

    # migrator.remove_model('famille')

    # migrator.remove_model('typeacte')

    # migrator.remove_model('naissance')


def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your rollback migrations here."""
    
    # @migrator.create_model
    # class Naissance(pw.Model):
    #     id = pw.AutoField()
    #     code_commune = pw.CharField(max_length=255)
    #     code_famille_acte = pw.CharField(max_length=255)
    #     numero_registre = pw.CharField(max_length=255)
    #     numero_acte = pw.CharField(max_length=255)
    #     code_etat = pw.CharField(max_length=255)
    #     code_sexe = pw.CharField(max_length=255)
    #     nom_principal = pw.CharField(max_length=255)
    #     prenom_principal = pw.CharField(max_length=255)
    #     lieu_naissance_principal = pw.CharField(max_length=255)
    #     date_naissance_principal = pw.DateField()
    #     rue_domicile_principal = pw.CharField(max_length=255)
    #     ville_domicile_principal = pw.CharField(default='NULL', max_length=255)
    #     nom_pere = pw.CharField(max_length=255)
    #     prenom_pere = pw.CharField(max_length=255)
    #     lieu_naissance_pere = pw.CharField(default='NULL', max_length=255)
    #     date_naissance_pere = pw.DateField()
    #     rue_domicile_pere = pw.CharField(default='NULL', max_length=255)
    #     ville_domicile_pere = pw.CharField(default='NULL', max_length=255)
    #     nom_mere = pw.CharField(default='NULL', max_length=255)
    #     prenom_mere = pw.CharField(default='NULL', max_length=255)
    #     lieu_naissance_mere = pw.CharField(default='NULL', max_length=255)
    #     date_naissance_mere = pw.DateField()
    #     rue_domicile_mere = pw.CharField(default='NULL', max_length=255)
    #     ville_domicile_mere = pw.CharField(default='NULL', max_length=255)
    #     date_evenement = pw.DateField()
    #     lieu_evenement = pw.CharField(default='NULL', max_length=255)
    #     heure_evenement = pw.TimeField()
    #     date_dresse = pw.DateField(default='NULL')
    #     heure_dresse = pw.TimeField(default='NULL')
    #     type_acte = pw.ForeignKeyField(column_name='type_acte_id', field='id', model=migrator.orm['typeacte'])
    #     famille = pw.ForeignKeyField(column_name='famille_id', field='id', model=migrator.orm['famille'])

    #     class Meta:
    #         table_name = "naissance"

    # @migrator.create_model
    # class TypeActe(pw.Model):
    #     id = pw.AutoField()
    #     nom_type_acte = pw.CharField(default='NULL', max_length=255)
    #     valeur = pw.CharField(default='NULL', max_length=255)
    #     famille = pw.ForeignKeyField(column_name='famille_id', default='NULL', field='id', model=migrator.orm['famille'])

    #     class Meta:
    #         table_name = "typeacte"

    # @migrator.create_model
    # class Famille(pw.Model):
    #     id = pw.AutoField()
    #     nom_famille = pw.CharField(default='NULL', max_length=255)
    #     cdc = pw.ForeignKeyField(column_name='cdc_id', default='NULL', field='id', model=migrator.orm['cdc'])

    #     class Meta:
    #         table_name = "famille"

    # @migrator.create_model
    # class Cdc(pw.Model):
    #     id = pw.AutoField()
    #     nom_cdc = pw.CharField(default='NULL', max_length=255)

    #     class Meta:
    #         table_name = "cdc"

    migrator.remove_model('roles')
