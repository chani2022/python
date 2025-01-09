from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from src.Gui.Admin.AdminMainWindow import Ui_adminWindow
from src.Model.RolesUser import Roles

class AdminWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_adminWindow()
        self.ui.setupUi(self)
        
        #initialement, on selectionne la premier tab
        self.ui.tabWidget.setCurrentIndex(0)
        self.tab_title = self.ui.tabWidget.tabText(self.ui.tabWidget.currentIndex())
        self.loadDataInCurrentTab()

        self.ui.tabWidget.currentChanged.connect(self.onTabChange) # event changement onglet

        #GESTION ROLES
        self.ui.btn_add_roles.clicked.connect(self.addObject) # evenement ajout
        self.ui.btn_delete_roles.clicked.connect(self.deleteObject) # evenement supprission
        #SIGNAL tableview
        self.ui.tableView_roles.clicked.connect(self.onCellClicked)
        #model a utiliser
        self.model = QStandardItemModel()
        

    def addObject(self):
        # print("mka", self.tab_title)
        match self.tab_title:
            case 'Rôle utilisateur':
                roles, ok = QInputDialog.getText(None, f"Ajout d'{self.tab_title}", "Roles :")
                if ok:
                    roles = roles.lower()
                    if Roles.select().where(Roles.type==roles).exists():
                        QMessageBox.critical(None, "Erreur", f"{roles} existe déjàs!")
                    else:
                        Roles.create(type = roles)
                        self.loadDataInCurrentTab()
                        

    def onTabChange(self, index):
        self.getCurrentTabTitle(index)
        print(self.tab_title)
        self.loadDataInCurrentTab()
    
    def loadDataInCurrentTab(self):
        objs = None
        # layout_main = QVBoxLayout()
        match self.tab_title:
            case 'Rôle utilisateur':
                objs = Roles.select()
                self.ui.tableView_roles.setModel(None) #on initialise chaque entree pour le mettre a jour à nouveau
                # self.model = QStandardItemModel()
                self.model.setHorizontalHeaderLabels(["Rôle"])
                for r in objs:
                    self.model.appendRow([QStandardItem(r.type)])
                self.ui.tableView_roles.setModel(self.model)


    def getCurrentTabTitle(self, index):
        self.tab_title = self.ui.tabWidget.tabText(index)

    def onCellClicked(self, index):
        value = self.model.data(index)
        match self.tab_title:
            case 'Rôle utilisateur':
                id_selected = Roles.select().where(Roles.type==value).get().id
                print(id_selected)
        print(value)

    def deleteObject(self):
        pass

