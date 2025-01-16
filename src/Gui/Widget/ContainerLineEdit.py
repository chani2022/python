from PyQt5.QtWidgets import QLineEdit, QGroupBox, QVBoxLayout
from src.Gui.Widget.DialogTableWidgetRegistre import DialogTableWidgetRegistre
from PyQt5.QtCore import pyqtSignal, Qt
from src.Gui.Widget.LineEdit import LineEdit

class ContainerLineEdit(QGroupBox):
    transfertRegistreAndChamps = pyqtSignal(object, object)
    nextPositionInStack = pyqtSignal(object)


    def __init__(self, cdc,champs = None):
        super().__init__()

        self.champs = champs
        self.cdc = cdc
        

        self.initChamps()

    def initChamps(self):
        self.setTitle(self.champs.label_champ if self.champs is not None else "Type de registre:")
        self.setStyleSheet("""
             QGroupBox {
                font-family: 'Papyrus';
                font-size: 20px;
                padding: 30 5px;
                background-color: #E8F5E9;
                width: 700px;
                border: none;
            }
            """)
        line_edit = LineEdit(self.champs, self.cdc)
        line_edit.transfertRegistreAndChamps.connect(self.onGetRegistreAndChamps)
        line_edit.transfertPositionStack.connect(self.transfertPosition)
        
        box_layout = QVBoxLayout()
        box_layout.addWidget(line_edit)
        self.setLayout(box_layout)


    def transfertPosition(self, position):
        self.nextPositionInStack.emit(position)
        
    def onGetRegistreAndChamps(self, registre, champs):
        self.transfertRegistreAndChamps.emit(registre, champs)


    