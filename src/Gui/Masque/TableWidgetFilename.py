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
            if i == 0:
                default_item = self.item(0, 0)
                self.setCurrentItem(default_item)
                # default_item.setSelected(True)
                default_item.setBackground(QColor("blue"))
        self.setColumnWidth(0, 400)

    def changeCurrentItem(self, row):
        rows = self.rowCount()
        for i in range(rows):
            item = self.item(i, 0)
            if row == i:
                self.setCurrentItem(item)
            item.setBackground(QColor("blue") if row == i else Qt.transparent)
        # for item in items:
        #     background = None
        #     if item.row() == row:
        #         background = "lightblue"
        #         self.setCurrentItem(item)
        #     item.setBackground(QColor(background))
        # item_selected = self.item(row, 0)
        # item_selected.setBackground(QColor("lightblue"))
        # item_selected.setSelected(True)

        # self.setCurrentItem(item_selected)
        
        

        

