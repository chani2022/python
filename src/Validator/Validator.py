from src.Date.DateTimeManager import DateTimeManager
from src.Repository.PrenomRepository import PrenomRepository
import re

class Validator:
        
    @classmethod
    def validate(self, line_edit_widget, champs, Famille, data):

        # self.app_state = AppState()

        name_widget_current = line_edit_widget.objectName()
        value = line_edit_widget.text()

        info = {
            "is_valid": True,
            "message": None,
            "value": value,
            "type": "critical"
        }
        
        for champ in champs:
            name = champ.name_champs
            label = champ.label_champ

            match Famille.cdc.nom_cdc:
                case 'LOG':
                    """
                        CDC LOGITIDE
                    """
                    if name_widget_current == name:
                        """
                        CHAMP OBLIGATOIRE DEFINIT DANS LA GESTION CHAMPS
                        """
                        if champ.obligatoire:
                            if info["value"] == "":
                                info["is_valid"] = False
                                info["message"] = f"{label} obligatoire!"

                                return info
                        
                        """
                        CONTROLE DES CHAMPS
                        """
                        """
                        informe l'utilisateur si le nom de l'enfant n'est pas le même du père
                        meme principe que la date d'évènement et date de dresse
                        """
                        if re.search(r'^nom', name_widget_current):
                            if re.search(r'pere|princi', name_widget_current):
                                nom_pere = None
                                nom_principal = None
                                is_nom_different = False
                                
                                for key in data:
                                    if re.search(r'^nom_pere', key):
                                        nom_pere = data[key]
                                    if re.search(r'^nom_principal', key):
                                        nom_principal = data[key]
                                
                                if nom_pere is None:
                                    if nom_principal and nom_principal != info["value"]:
                                        is_nom_different = True
                                if nom_principal is None:
                                    if nom_pere and info["value"] != nom_pere:
                                        is_nom_different = True
                                    # print(is_nom_different)

                                if is_nom_different:
                                    info["is_valid"] = False
                                    info["message"] = f"Le nom de l'enfant est different du père! \n Voulez-vous continuer?"
                                    info["type"] = "question"
                        """
                        pour le prenom,
                        check dans la base si chaque prénom y trouve,
                        si on ne le trouve pas
                        informe l'utilisateur s'il veut continuer
                        sinon
                        mettre en miniscule
                        supprimer l'espace avant et après
                        remplace l'espace par virgule
                        """
                        if re.search(r'^prenom', name_widget_current):
                            """
                            pour les prenom n'ont obligatoire, mais renseigner
                            """
                            if info["value"] != "":
                                prenoms_not_found = Validator.checkPrenom(info["value"].lower())

                                if len(prenoms_not_found) > 0:
                                    info["message"] = f"Les prénoms <strong>({', '.join(prenoms_not_found)})</strong> ne sont pas répertoriés.\nVoulez-vous continuer?"
                                    info["type"] = "question"
                                    info["is_valid"] = False
                                else:
                                    info['value'] = re.sub(r" +", ", ", info["value"].strip().lower().title())#capital initiale
                                    if re.search(r'princip', name_widget_current):
                                        info['value'] = info['value'].upper()
                                    
                        """
                        pour le sexe, valeur possible (1, 2, 3)
                        """
                        if re.search(r'sexe', name):
                            if value != '1' and value != '2' and value != '3':
                                info['is_valid'] = False
                                info['message'] = f"{label} invalide! valeur possible (1 ou 2 ou 3)"
                        """
                        cast le string numero d'acte
                        pour gerer le numero d'acte dynamiquement
                        """
                        if re.search(r'numero', name_widget_current):
                            if re.search(r'acte', name_widget_current):
                                info["is_valid"] = False
                                # info["type"] = None
                                try:
                                    info["value"] = int(info["value"])
                                    info["type"] = "castNumeroActeOk"
                                except ValueError:
                                    info["value"] = info["value"]
                                    info["type"] = "castNumeroActeFailed"

                        if re.search(r'^date', name_widget_current):
                            if re.search(r'even|dres|naissa',name_widget_current):
                                """
                                pour les champs qui ne sont pas obligatoire,
                                on le laisse passer le contenu vide
                                """
                                if info["value"] != "":
                                    day = None
                                    month = None
                                    year = None

                                    if not DateTimeManager.isDateValid(info["value"]):
                                        info["is_valid"] = False
                                        info["message"] = f"{label} invalide! Format valide JJMMAAAA"
                                    else:
                                        day = info["value"][0:2]
                                        month = info["value"][2:4]
                                        year = info["value"][4:8]
                                        info["value"] = f"{year}{month}{day}"
                                        info["value"] = DateTimeManager.convertStringToDate(info["value"], f"%Y%m%d")
                                    
                                        """
                                            A PARTIR D'ICI, INFO['value'] EST UNE DATETIME
                                        """
                                        if re.search(r'even|dress', name_widget_current):
                                            numero_registre = data["numero_registre"][0:4]#extraire l'année s'il y a bis
                                            """
                                            on informe l'utilisateur
                                            si l'année de registre est different de annee de dresse ou evenement
                                            """
                                            if int(numero_registre) != int(year):
                                                info["is_valid"] = False
                                                info["message"] = f"La {label} est different de l'année de registre\n Voulez-vous continuer?"
                                                info["type"] = "question"
                                            
                                            """
                                            lors de la première passage soit le date d'évènement ou date dresse, 
                                            on stocke sa valeur sous forme de date dans l'attribut data de la fenetre main,
                                            puis lors de la deuxième passage,
                                            on check le date stocke et la valeur courant, s'il y a une erreur, on l'informe l'utilisateur
                                            """
                                            date_evenement = None
                                            date_dresse = None
                                            is_date_dresse_lower = False

                                            for key in data:
                                                if re.search(r'even', key):
                                                    date_evenement = data[key]
                                                if re.search(r'dres', key):
                                                    date_dresse = data[key]
        
                                            if date_evenement is None:
                                                if date_dresse and date_dresse < info["value"]:
                                                    is_date_dresse_lower = True
                                            if date_dresse is None:
                                                if date_evenement and info["value"] < date_evenement:
                                                    is_date_dresse_lower = True

                                            if is_date_dresse_lower:
                                                info["is_valid"] = False
                                                info["message"] = f"la date de dresse < date d'évènement \n Voulez-vous continuer?"
                                                info["type"] = "question"
                                    
                        if re.search(r'heure', name_widget_current):
                            """
                            pour les champs qui ne sont pas obligatoire,
                            on le laisse passer le contenu vide,
                            sinon on check la valeur
                            """
                            if info["value"] != "":
                                if not DateTimeManager.isTimeValid(info["value"]):
                                    info["is_valid"] = False
                                    info["message"] = f"{label} invalide! Format valide HHMM"
                                else:
                                    info["value"] = DateTimeManager.convertStringToHours(info["value"])

        return info
    
    @staticmethod
    def checkNumeroRegistre(numero_registre, nom_cdc_current):
        info = {
            "is_valid": True,
            "message": None,
            "value": numero_registre,
            "type": "critical"
        }
        match nom_cdc_current:
            case 'LOG':
                """
                    POUR LE CDC LOG
                """
                if len(numero_registre) > 7:
                    # MessageBox.show("critical", "Année de registre trop long")
                    info["is_valid"] = False
                    info["message"] = "Année de registre trop long"
                    # return
                else:
                    if len(numero_registre) == 4:
                        if not DateTimeManager.isYearValid(numero_registre):
                            # MessageBox.show("critical", "Année de registre invalid")
                            info["is_valid"] = False
                            info["message"] = "Année de registre invalid"
                            # return
                    elif len(numero_registre) < 3:
                        info["is_valid"] = False
                        info["message"] = "Année de registre trop court"
                        # return
                    else:
                        date = numero_registre[:4]
                        if not DateTimeManager.isYearValid(date):
                            # MessageBox.show("critical", "Année de registre invalid")
                            info["is_valid"] = False
                            info["message"] = "Année de registre invalid"
                        
        return info

    @staticmethod
    def checkPrenom(value_prenoms:str)->list:
        prenoms_not_found = list()
                  
        list_prenoms = value_prenoms.split()
        prenoms = PrenomRepository.findPrenoms(list_prenoms)

        """
        recuperer les prénoms introuvables
        """
        for pre in list_prenoms:
            is_prenom_found = False
            for prenom in prenoms:
                if pre.lower() == prenom.prenom.lower():
                    is_prenom_found = True
                    break

            if not is_prenom_found:
                prenoms_not_found.append(pre)

        return prenoms_not_found



        
