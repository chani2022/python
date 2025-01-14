from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QMessageBox
from PyQt5.uic import loadUi
from src.Model.User import User
from src.Model.RolesUser import Roles
from src.PasswordManager.PasswordManager import PasswordManager
from peewee import fn

class DialogUser(QDialog):

    def __init__(self):
        super().__init__()

        loadUi('src/Gui/Admin/dialogUser.ui', self)
        self.init()

        self.input_nom.setFocus()
        
        self.btn_add.clicked.connect(self.onAddUser)

    def init(self):
        self.table_widget_utilisateur.setRowCount(User.select().count())
        self.table_widget_utilisateur.setColumnCount(4)
        self.table_widget_utilisateur.setHorizontalHeaderLabels(["Matricule","Nom", "Prénom", "roles"])
        for i,user in enumerate(User.select()):
            info = [ str(user.matricule), user.nom, user.prenom, user.roles.type ]
            for j, data in enumerate(info):
                width_column = 125
                if j == 0:
                    width_column = 75
                self.table_widget_utilisateur.setItem(i,j, QTableWidgetItem(data))
                self.table_widget_utilisateur.setColumnWidth(j, width_column)

    def onAddUser(self):
        nom = self.input_nom.text().upper()
        prenom = self.input_prenom.text().capitalize()
        matricule_max = User.select(fn.MAX(User.matricule)).scalar()
        roles = Roles.select().where(Roles.type=="user").get()
        password_manager = PasswordManager()
        password_hashed = password_manager.hashPassword("user")

        User.create(nom=nom, prenom=prenom, password=password_hashed, matricule=matricule_max+1, roles=roles)

        self.input_nom.setText("")
        self.input_prenom.setText("")
        QMessageBox.information(self, "Identification", f"Votre identifiant est {matricule_max+1} et mot de passe: user")

        self.init()
    

