from src.Model.Production import Production
from src.Model.Champs import Champs
from src.Singleton.AppState import AppState
from peewee import JOIN, fn     

class ProductionRepository():

    def __init__(self):
        self.app_state = AppState()

    def findDataPreviousActe(self, cdc, registre, user, annee):
        productions = (Production
                 .select(Production)
                 .join(Champs, JOIN.LEFT_OUTER)
                 .where(
                    (Production.cdc == cdc) &
                    (Production.registre == registre) &
                    (Production.user == user) &
                    (Production.numero_acte == self.app_state.numero_acte) &
                    (Production.annee_registre == annee) & 
                    (Production.numero_acte == self.app_state.numero_acte))
                ).order_by(Champs.position)
        data = []
        for production in productions:

            name = None
            label = None
            valeur = production.valeur_champ

            if production.champs is None:
                name = "type_registre"
                label = "Type de registre"
            else:
                name = production.champs.name_champs
                label = production.champs.label_champ
            info = {"name": name, "label": label, "valeur": valeur}
            data.append(info)
        return data
    # def findAll
    def findLastRecord(self):
        pass

    def findAllGroupBy(self, cdc, registre, annee):
        productions = (Production
                        .select()
                        .join(Champs, JOIN.LEFT_OUTER)
                        .where(
                            (Production.cdc == cdc) &
                            (Production.registre == registre) &
                            (Production.annee_registre == annee)
                        )
                        .order_by(Production.numero_acte))
        return productions
        