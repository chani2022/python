# # from src.Model.Production import Production
# from src.Model.Champs import Champs
# from peewee import JOIN, fn 
# from datetime import date


# class ProductionRepository():

#     def __init__(self):

#     def findDataPreviousActe(self, cdc, registre, user, annee):
#         pass
#         # productions = (Production
#         #          .select(Production)
#         #          .join(Champs, JOIN.LEFT_OUTER)
#         #          .where(
#         #             (Production.cdc == cdc) &
#         #             (Production.registre == registre) &
#         #             (Production.user == user) &
#         #             (Production.numero_acte == self.app_state.numero_acte) &
#         #             (Production.annee_registre == annee) & 
#         #             (Production.numero_acte == self.app_state.numero_acte))
#         #         ).order_by(Champs.position)
#         # data = []
#         # for production in productions:

#         #     name = None
#         #     label = None
#         #     valeur = production.valeur_champ

#         #     if production.champs is None:
#         #         name = "type_registre"
#         #         label = "Type de registre"
#         #     else:
#         #         name = production.champs.name_champs
#         #         label = production.champs.label_champ
#         #     info = {"name": name, "label": label, "valeur": valeur}
#         #     data.append(info)
#         # return data
#     # def findAll
#     def findLastRecord(self):
#         pass

#     def findAll(self, cdc, registre, annee, user):
#         pass
#         # productions = (Production
#         #                 .select()
#         #                 .join(Champs, JOIN.LEFT_OUTER)
#         #                 .where(
#         #                     (Production.cdc == cdc) &
#         #                     (Production.registre == registre) &
#         #                     (Production.annee_registre == annee) & 
#         #                     (Production.user == user)
#         #                 )
#         #                 .order_by(Production.numero_acte))
#         # return productions
    
#     def findAllPresentDay(self, cdc, registre, annee, user):
#         pass
#         # today = date.today()
#         # productions = (Production
#         #                 .select()
#         #                 .join(Champs, JOIN.LEFT_OUTER)
#         #                 .where(
#         #                     (Production.cdc == cdc) &
#         #                     (Production.registre == registre) &
#         #                     (Production.annee_registre == annee) & 
#         #                     (Production.user == user) &
#         #                     (fn.date(Production.date_traitement) == today) #ignore l' heure
#         #                 )
#         #                 .order_by(Production.numero_acte))
#         # return productions


#     def findLast10Records(self, cdc, registre, annee):
#         pass
#         # productions = (Production
#         #                 .select(Production, fn.COUNT(Production.numero_acte).alias("count"))
#         #                 .join(Champs, JOIN.LEFT_OUTER)
#         #                 .where(
#         #                     (Production.cdc == cdc) &
#         #                     (Production.registre == registre) &
#         #                     (Production.annee_registre == annee)
#         #                 )
#         #                 .order_by(Production.numero_acte.desc())
#         #                 .group_by(Production.numero_acte))
#         #                 # .limit(100))

#         # return productions
    
#     @classmethod
#     def insertMultipleData(self, data):
#         pass
#         # Production.insert_many(
#         #     data, 
#         #     fields=[
#         #         Production.cdc, 
#         #         Production.registre, 
#         #         Production.user, 
#         #         Production.date_traitement,
#         #         Production.annee_registre,
#         #         Production.valeur_champ, 
#         #         Production.numero_acte,
#         #         Production.champs,
#         #         Production.nom_image,
                
#         # ]).execute()
        