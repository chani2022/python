from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from src.Model.TypeActe import TypeActe

class DialogAddTypeActe(QDialog):

    def __init__(self, famille):
        super().__init__()

        loadUi('src/Gui/Admin/DialogAddTypeActe.ui', self)
        
        self.famille = famille
        self.btn_add_type_acte.clicked.connect(self.onAddTypeActe)

        self.resize(700, 150)

    def onAddTypeActe(self):
        nom_type_acte = self.input_nom.text().capitalize()
        valeur = self.input_valeur.text().upper()
        type_acte_exists = TypeActe.select().where(
            (TypeActe.nom_type_acte == nom_type_acte) | (TypeActe.valeur == valeur)).exists()
        if type_acte_exists:
            QMessageBox.warning(self, 'Attention', f"{nom_type_acte} ou {valeur} existe déjà")
            return
        elif nom_type_acte == "" and valeur == "":
            QMessageBox.critical(self, 'Erreur', "Tous les champs sont obligatoire", QMessageBox.Yes, QMessageBox.Yes)
            return
        else:            
            TypeActe.create(nom_type_acte=nom_type_acte, valeur=valeur, famille=self.famille)
            self.input_nom.setText("")
            self.input_valeur.setText("")
            self.input_nom.setFocus()

