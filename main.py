import sys
from PyQt5 import QtWidgets
from src.Gui.Connexion.Connexion import Ui_Connexion
from src.Model.User import User
from src.Model.RolesUser import Roles
from src.PasswordManager.PasswordManager import PasswordManager

if __name__ == "__main__":

    # list_roles = ["admin", "user"]
    # admin = None
    # for r in list_roles:
    #     ro = Roles.create(type=r)
    #     if ro.type == "admin":
    #         admin = ro
    
    
    # #ajouter une administrateur
    # password_hashed = PasswordManager.hashPassword(plain_password="admin")
    # #création d'un administrateur
    # User.create(nom="ANDRIANARINAIVO", prenom="Chani", matricule=1, password=password_hashed, roles=admin)

    app = QtWidgets.QApplication(sys.argv)
    Connexion = QtWidgets.QWidget()
    ui = Ui_Connexion()
    ui.setupUi(Connexion)
    Connexion.show()
    sys.exit(app.exec_())