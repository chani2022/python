from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, pyqtSignal
from src.Model.Registre import Registre
from src.Model.Champs import Champs

class DialogTableWidgetRegistre(QDialog):

    returnPressed = pyqtSignal(object, object)

    def __init__(self, cdc):
        super().__init__()

        self.cdc = cdc

        loadUi('src/Gui/Widget/dialogTableWidgetRegistre.ui', self)

        self.initRegistre()
        # self.table_widget_registre.cellEntered.connect(self.onOkPressed)

    def initRegistre(self):
        registres = Registre.select().where(Registre.cdc == self.cdc).order_by(Registre.id)
        self.table_widget_registre.setRowCount(len(registres))
        self.table_widget_registre.setColumnCount(1)
        self.table_widget_registre.setHorizontalHeaderLabels(["Type de registre"])

        for i, registre in enumerate(registres):
            self.table_widget_registre.setItem(i, 0, QTableWidgetItem(registre.type_registre))
            self.table_widget_registre.setColumnWidth(0, 400)

    def keyPressEvent(self, event):
        # Vérifie si la touche pressée est "Return" ou "Enter"
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            text_item_selected = self.table_widget_registre.item(self.table_widget_registre.currentRow(),0).text()
            registre = Registre.select().where(Registre.type_registre == text_item_selected).get()
            champs = (
                        Champs
                        .select()
                        .where(Champs.registre == registre)
                        .order_by(Champs.position)
                    )
            
            self.returnPressed.emit(registre, champs)
            self.accept() # on ferme la boite de dialogue

            
    

    
