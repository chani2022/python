from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtCore import pyqtSignal

class TableWidgetFilename(QTableWidget):

    cellClickedSignal = pyqtSignal(int, int)  # Signal personnalisé pour les clics sur les cellules

    def __init__(self):
        super().__init__()

        self.index_row_selected = 0
        self.cellClicked.connect(self.emitCellClicked)

    def appendRow(self, list_images):
        max_row = len(list_images)
        max_column = 1
        self.setRowCount(max_row)
        self.setColumnCount(max_column)
        self.setHorizontalHeaderLabels(["nom du fichier"])
        for i,filename in enumerate(list_images):
            self.setItem(i,0, QTableWidgetItem(filename))
            if i == 0:
                default_item = self.item(0, 0)
                self.setCurrentItem(default_item)
                default_item.setSelected(True)
        self.setColumnWidth(0, 400)

    def changeCurrentItem(self, row):
        item_selected = self.item(row, 0)
        self.setCurrentItem(item_selected)
        item_selected.setSelected(True)

    def emitCellClicked(self, row, column):
        self.cellClickedSignal.emit(row, column)
        # self.index_row_selected = row
        # print(row)
        # if hasattr(self.parent(), "stacked_widget_images"):
        #     print(row)
        #     self.parent().tableWidgetClicked(row)

        

