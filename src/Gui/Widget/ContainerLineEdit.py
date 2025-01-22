from PyQt5.QtWidgets import QLineEdit, QGroupBox, QVBoxLayout
from src.Gui.Widget.DialogTableWidgetRegistre import DialogTableWidgetRegistre
from PyQt5.QtCore import pyqtSignal, Qt
from src.Gui.Widget.LineEdit import LineEdit

class ContainerLineEdit(QGroupBox):
    childrenFindRegistreAndChamps = pyqtSignal(object, object)
    nextPositionInStack = pyqtSignal(object)
    previousPositionInStack = pyqtSignal(object)
    zoom = pyqtSignal(object)
    scrollDefile = pyqtSignal(object, object)


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
                width: 700px;
            }
            """)
        line_edit = LineEdit(self.champs, self.cdc)
        line_edit.registreAndChampsSelected.connect(self.onGetRegistreAndChamps)
        line_edit.tabPressed.connect(self.transfertPosition)
        line_edit.EscapePressed.connect(self.transfertPositionPrevious)
        line_edit.ctrlPressed.connect(self.transfertZoom)
        line_edit.ctrlDirectionPressed.connect(self.moveScroll)
        
        box_layout = QVBoxLayout()
        box_layout.addWidget(line_edit)
        self.setLayout(box_layout)


    def transfertPosition(self, position):
        self.nextPositionInStack.emit(position)

    def transfertPositionPrevious(self, position):
        self.previousPositionInStack.emit(position)
        
    def onGetRegistreAndChamps(self, registre, champs):
        self.childrenFindRegistreAndChamps.emit(registre, champs)

    def transfertZoom(self, is_zoom_plus):
        self.zoom.emit(is_zoom_plus)

    def moveScroll(self, arrow_pressed, step):
        self.scrollDefile.emit(arrow_pressed, step)


    