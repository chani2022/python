from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, pyqtSignal
from src.Model.TypeActe import TypeActe
from src.Model.Champs import Champs

class DialogTableWidgetTypeActe(QDialog):

    getTypeActe = pyqtSignal(object)

    def __init__(self, famille):
        super().__init__()

        self.famille = famille

        loadUi('src/Gui/Masque/dialogTableWidgetTypeActe.ui', self)

        self.initRegistre()
        self.resize(500, 275)

    def initRegistre(self):
        type_actes = TypeActe.select().where(TypeActe.famille == self.famille).order_by(TypeActe.id)
        self.table_widget_type_acte.setRowCount(len(type_actes))
        self.table_widget_type_acte.setColumnCount(2)
        self.table_widget_type_acte.setHorizontalHeaderLabels(["Type d'acte", "valeur"])

        for row, type_acte in enumerate(type_actes):
            infos = [type_acte.nom_type_acte, type_acte.valeur]
            for col, info in enumerate(infos):
                width = 60
                if col == 1:
                    width = 325
                self.table_widget_type_acte.setItem(row, col, QTableWidgetItem(info))
                self.table_widget_type_acte.setColumnWidth(0, width)

    def keyPressEvent(self, event):
        # Vérifie si la touche pressée est "Return" ou "Enter"
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            text_item_selected = self.table_widget_type_acte.item(self.table_widget_type_acte.currentRow(),1).text()
            type_acte = TypeActe.select().where(TypeActe.valeur == text_item_selected).get()
            self.getTypeActe.emit(type_acte)
            self.accept() # on ferme la boite de dialogue

            
    

    
