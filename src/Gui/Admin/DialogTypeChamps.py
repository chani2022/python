from PyQt5.QtWidgets import QDialog, QInputDialog, QTableWidgetItem
from PyQt5.uic import loadUi

class DialogTypeChamps(QDialog):

    def __init__(self):
        super().__init__()
        loadUi('src/Gui/Admin/dialogTypeChamps.ui', self)

        self.init()

        self.btn_add_type_champs.clicked.connect(self.onAddTypeChamps)

    
    def init(self):
        pass
        # self.table_widget_type_champs.setRowCount(TypeChamps.select().count())
        # self.table_widget_type_champs.setColumnCount(1)
        # self.table_widget_type_champs.setHorizontalHeaderLabels(["Type de champs"])
        # for i,role in enumerate(TypeChamps.select()):
        #     self.table_widget_type_champs.setItem(i,0, QTableWidgetItem(role.type_champs))
        # self.table_widget_type_champs.setColumnWidth(0, 150)

    def onAddTypeChamps(self):
        pass
        # text, ok = QInputDialog.getText(self, "Ajout type de champs", "type de champs:")
        # if ok:
        #     TypeChamps.create(type_champs=text)
        #     self.init()

