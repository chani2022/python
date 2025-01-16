from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal, Qt
from src.Model.Ville import Ville


class DialogBaseVille(QDialog):

    textRowSelected = pyqtSignal(str, str)

    def __init__(self, keyword):
        super().__init__()

        loadUi('src/Gui/BaseVille/baseVille.ui', self)

        villes = Ville.select().where(Ville.ville ** f"%{keyword}%") # Opérateur `ILIKE` natif insensible à la case
        self.table_widget_ville.setRowCount(len(villes))
        self.table_widget_ville.setColumnCount(4)
        self.table_widget_ville.setHorizontalHeaderLabels(["Ville", "Département", "Région", "Code commune"])

        self.resize(750, 300)

        for i, ville in enumerate(villes):
            infos = [ville.ville, ville.departement, ville.region, ville.code_commune]
            for j, info in enumerate(infos):
                if info is None:
                    info = ""
                self.table_widget_ville.setItem(i, j, QTableWidgetItem(str(info)))
                self.table_widget_ville.setColumnWidth(j, 250)


    def keyPressEvent(self, event):
        # Vérifie si la touche pressée est "Return" ou "Enter"
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            current_row = self.table_widget_ville.item(self.table_widget_ville.currentRow(),0)
            #si aucun choix n'est proposé, on ferme la dialog et on arrete la
            if current_row is None:
                self.accept()
                return
            
            ville = self.table_widget_ville.item(self.table_widget_ville.currentRow(),0).text()
            departement = self.table_widget_ville.item(self.table_widget_ville.currentRow(), 1).text()
            
            self.textRowSelected.emit(ville, departement)
            self.accept() # on ferme la boite de dialogue

    