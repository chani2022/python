from src.Model.Naissance import Naissance

class NaissanceRepository:

    @staticmethod
    def saveData(data: dict):

        Naissance.create(
            code_commune=data["code_commune"],
            code_famille_acte= data['code_famille_acte'],
            code_etat=data['code_etat'],
            numero_registre=data['numero_registre'],
            user=data['user'],
            date_evenement=data['date_evenement'],
            date_dresse=data['date_dresse'],
            numero_acte=data['numero_acte'],
            date_naissance_pere=data['date_naissance_pere'],
            ville_domicile_mere=data['ville_domicile_mere'],
            code_sexe=data['code_sexe'],
            date_naissance_mere=data['date_naissance_mere'],
            nom_principal=data['nom_principal'],
            prenom_principal=data['prenom_principal'],
            rue_domicile_principal=data['rue_domicile_principal'],
            ville_domicile_principal=data['ville_domicile_principal'],
            nom_pere=data['nom_pere'],
            prenom_pere=data['prenom_pere'],
            lieu_naissance_pere=data['lieu_naissance_pere'],
            rue_domicile_pere=data['rue_domicile_pere'],
            ville_domicile_pere=data['ville_domicile_pere'],
            nom_mere=data['nom_mere'],
            prenom_mere=data['prenom_mere'],
            rue_domicile_mere=data['rue_domicile_mere'],
            lieu_evenement=data['lieu_evenement'],
            heure_dresse=data['heure_dresse'],
            type_acte=data['type_acte'],
            lieu_naissance_principal=data['lieu_naissance_principal'],
            date_naissance_principal=data['date_naissance_principal'],
            lieu_naissance_mere=data['lieu_naissance_mere'],
            heure_evenement=data['heure_evenement'],
            famille=data['famille'],
            date_traitement=data['date_traitement'],
            heure_traitement=data['heure_traitement'],
            nom_fichier = data['nom_fichier'],
            annotation= data['annotation']
            )
        
    @staticmethod
    def acteExist(Famille: object, numero_acte: str, numero_registre: str) -> bool:
        return Naissance.select().where(
            (Naissance.famille == Famille) & (Naissance.numero_acte == numero_acte) & (Naissance.numero_registre == numero_registre)
            ).exists()
    
    @staticmethod
    def getOneActe(Famille: object, numero_acte: str, numero_registre) -> Naissance|None:
        return Naissance.select().where(
            (Naissance.famille == Famille) & (Naissance.numero_acte == numero_acte) & (Naissance.numero_registre == numero_registre)
        ).get()
    
    @staticmethod 
    def updateActe(data: dict, id_naisssance: int):
        q = Naissance.update(
            code_commune=data["code_commune"],
            code_famille_acte= data['code_famille_acte'],
            code_etat=data['code_etat'],
            numero_registre=data['numero_registre'],
            user=data['user'],
            date_evenement=data['date_evenement'],
            date_dresse=data['date_dresse'],
            numero_acte=data['numero_acte'],
            date_naissance_pere=data['date_naissance_pere'],
            ville_domicile_mere=data['ville_domicile_mere'],
            code_sexe=data['code_sexe'],
            date_naissance_mere=data['date_naissance_mere'],
            nom_principal=data['nom_principal'],
            prenom_principal=data['prenom_principal'],
            rue_domicile_principal=data['rue_domicile_principal'],
            ville_domicile_principal=data['ville_domicile_principal'],
            nom_pere=data['nom_pere'],
            prenom_pere=data['prenom_pere'],
            lieu_naissance_pere=data['lieu_naissance_pere'],
            rue_domicile_pere=data['rue_domicile_pere'],
            ville_domicile_pere=data['ville_domicile_pere'],
            nom_mere=data['nom_mere'],
            prenom_mere=data['prenom_mere'],
            rue_domicile_mere=data['rue_domicile_mere'],
            lieu_evenement=data['lieu_evenement'],
            heure_dresse=data['heure_dresse'],
            type_acte=data['type_acte'],
            lieu_naissance_principal=data['lieu_naissance_principal'],
            date_naissance_principal=data['date_naissance_principal'],
            lieu_naissance_mere=data['lieu_naissance_mere'],
            heure_evenement=data['heure_evenement'],
            famille=data['famille'],
            date_traitement=data['date_traitement'],
            heure_traitement=data['heure_traitement'],
            nom_fichier = data['nom_fichier'],
            annotation= data['annotation']
            ).where(Naissance.id == id_naisssance)
        
        q.execute()

    @staticmethod
    def count(Famille: object, numero_registre:int)->int:
        return Naissance.select().where(
            (Naissance.famille == Famille) & (Naissance.numero_registre == numero_registre)
            ).count()
    
    @staticmethod
    def getLastActes(Famille: object, numero_registre: str, limit: int = 10):
        return (Naissance.select()
                .where(
                        (Naissance.famille == Famille) & (Naissance.numero_registre == numero_registre)
                )
                .order_by(Naissance.numero_acte)
                .limit(limit)
                .order_by(Naissance.numero_acte))
        

