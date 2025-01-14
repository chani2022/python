from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QInputDialog, QMessageBox
from PyQt5.uic import loadUi
from src.Model.RolesUser import Roles

class DialogRoles(QDialog):

    def __init__(self):
        super().__init__()
        loadUi('src/Gui/Admin/DialogRoles.ui', self)
        self.id_selected = None

        self.init()

        self.table_widget_roles.cellClicked.connect(self.onCellTableWidgetClicked)

        #signal bouton
        self.btn_add.clicked.connect(self.onAddRoles)
        self.btn_delete.clicked.connect(self.onDeleteRole)

    def onCellTableWidgetClicked(self, row, column):
        text_selected = self.table_widget_roles.item(row, column).text()
        self.id_selected = Roles.select().where(Roles.type == text_selected).get().id

    def onAddRoles(self):
        text, ok = QInputDialog.getText(self, "Ajout roles", "Role:")
        if ok:
            Roles.create(type=text)
            self.init()
        pass
    def onDeleteRole(self):
        if self.id_selected == None:
            QMessageBox.critical(self, "Erreur", "Veuillez selectionner une role à supprimer")
            return
        reply = QMessageBox.question(self, "confirmation", "Voulez-vous vraiment supprimer?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            Roles.delete_by_id(self.id_selected)
            self.init()
        self.id_selected = None #pour que l'utilisateur soit informé s'il ne selectionne aucune element

    def init(self):
        self.table_widget_roles.setRowCount(Roles.select().count())
        self.table_widget_roles.setColumnCount(1)
        self.table_widget_roles.setHorizontalHeaderLabels(["Roles"])
        for i,role in enumerate(Roles.select()):
            self.table_widget_roles.setItem(i,0, QTableWidgetItem(role.type))
        self.table_widget_roles.setColumnWidth(0, 400)

        






