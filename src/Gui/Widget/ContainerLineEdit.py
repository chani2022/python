from PyQt5.QtWidgets import QLineEdit, QGroupBox, QVBoxLayout
# from src.Gui.Widget.DialogTableWidgetRegistre import DialogTableWidgetRegistre
from PyQt5.QtCore import pyqtSignal, Qt
from src.Gui.Widget.LineEdit import LineEdit

class ContainerLineEdit(QGroupBox):
    # onGetTypeActe = pyqtSignal(object)
    nextPositionInStack = pyqtSignal()
    previousPositionInStack = pyqtSignal()
    zoom = pyqtSignal(object)
    scrollDefile = pyqtSignal(object, object)


    def __init__(self, famille, champs, numero_acte):
        super().__init__()

        self.champs = champs
        self.famille = famille
        self.numero_acte = numero_acte
        # self.cdc = cdc

        self.initChamps()

    def initChamps(self):
        self.setTitle(self.champs.label_champ)
        self.setStyleSheet("""
             QGroupBox {
                font-family: 'Papyrus';
                font-size: 20px;
                padding: 30 5px;
                width: 700px;
            }
            """)
        #mettre en subrillance si obligatoire
        if self.champs.obligatoire:
            self.setStyleSheet("""
             QGroupBox {
                font-family: 'Papyrus';
                font-size: 20px;
                padding: 30 5px;
                width: 700px;
                color: 'red'
            }
            """)
        line_edit = LineEdit(self.champs, self.famille, self.numero_acte)
        # line_edit.onGetTypeActe.connect(self.onReturnTypeActe)
        line_edit.tabPressed.connect(self.nextField)
        line_edit.escapePressed.connect(self.previousField)
        line_edit.ctrlPressed.connect(self.transfertZoom)
        line_edit.ctrlDirectionPressed.connect(self.moveScroll)
        
        box_layout = QVBoxLayout()
        box_layout.addWidget(line_edit)
        self.setLayout(box_layout)


    def nextField(self):
        self.nextPositionInStack.emit()

    def previousField(self):
        self.previousPositionInStack.emit()
        
    # def onReturnTypeActe(self, TypeActe):
    #     self.onGetTypeActe.emit(TypeActe)

    def transfertZoom(self, is_zoom_plus):
        self.zoom.emit(is_zoom_plus)

    def moveScroll(self, arrow_pressed, step):
        self.scrollDefile.emit(arrow_pressed, step)


    