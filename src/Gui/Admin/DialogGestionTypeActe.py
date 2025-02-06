from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
# from src.Model.Champs import Champs
from src.Model.TypeActe import TypeActe
# from src.Model.TypeChamps import TypeChamps
from src.Gui.Admin.DialogAddTypeActe import DialogAddTypeActe

class DialogGestionTypeActe(QDialog):

    def __init__(self, famille):
        super().__init__()
        loadUi('src/Gui/Admin/dialogGestionTypeActe.ui', self)

        # self.type_actes = type_actes
        self.famille = famille
        self.type_acte_selected = None
        self.champs_selected = None
        
        self.initTypeActe()
        self.group_box_type_acte.setTitle(f"Type Actes ({famille.nom_famille})")
        
        """
        signal type acte
        """
        self.btn_add_type_acte.clicked.connect(self.onAddTypeActe)
        self.btn_delete_type_acte.clicked.connect(self.onDeleteTypeActe)
        self.table_widget_type_acte.cellClicked.connect(self.onCellTypeActeTableWidgetClicked)

        self.resize(1200, 350)

    def initTypeActe(self):
        self.type_actes = TypeActe.select().where(TypeActe.famille == self.famille)
        self.table_widget_type_acte.setRowCount(len(self.type_actes))
        self.table_widget_type_acte.setColumnCount(2)
        self.table_widget_type_acte.setHorizontalHeaderLabels(["Nom", "Valeur"])
        for row, type_acte in enumerate(self.type_actes):
            infos = [type_acte.nom_type_acte, type_acte.valeur]
            for col, info in enumerate(infos):
                self.table_widget_type_acte.setItem(row, col, QTableWidgetItem(info))
                self.table_widget_type_acte.setColumnWidth(0, 250)

    def onAddTypeActe(self):
        dialog_add_type_acte = DialogAddTypeActe(self.famille)
        dialog_add_type_acte.exec_()
        self.initTypeActe()

    def onDeleteTypeActe(self):
        if self.type_acte_selected is None:
            QMessageBox.warning(self, "Attention", "Aucun type acte n'est selectionné")
            return
        reply = QMessageBox.question(self, "Question", f"Voulez vous vraiment supprimer {self.type_acte_selected.nom_type_acte}?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            TypeActe.delete_by_id(self.type_acte_selected)
            self.type_acte_selected = None
            self.initTypeActe()

    def onCellTypeActeTableWidgetClicked(self, row):
        text_selected = self.table_widget_type_acte.item(row, 0).text()
        self.type_acte_selected = TypeActe.select().where(TypeActe.nom_type_acte == text_selected).get()



    
