from src.Model.Prenom import Prenom

class PrenomRepository:

    @staticmethod
    def findPrenoms(prenoms: list):
        return Prenom.select().where(Prenom.prenom.in_(prenoms)).order_by(Prenom.prenom.asc())