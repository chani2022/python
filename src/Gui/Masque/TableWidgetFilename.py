from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal

class TableWidgetFilename(QTableWidget):

    def __init__(self):
        super().__init__()

        self.index_row_selected = 0

    def appendRow(self, list_images):
        max_row = len(list_images)
        max_column = 1
        self.setRowCount(max_row)
        self.setColumnCount(max_column)
        self.setHorizontalHeaderLabels(["Nom du fichier"])
        for i,filename in enumerate(list_images):
            self.setItem(i,0, QTableWidgetItem(filename))
        self.setColumnWidth(0, 400)

    def changeCurrentItem(self, row):
        """
        mettre en subrillance la ligne selectionner
        et les autres, couleur par default
        """
        rows = self.rowCount()
        for i in range(rows):
            item = self.item(i, 0)
            if row == i:
                self.setCurrentItem(item)
            item.setBackground(QColor("blue") if row == i else Qt.transparent)
        
        

        

