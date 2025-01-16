from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt, QEvent, pyqtSignal
from src.Gui.Widget.DialogTableWidgetRegistre import DialogTableWidgetRegistre
from src.Singleton.AppState import AppState
from src.Gui.BaseVille.DialogBaseVille import DialogBaseVille

class LineEdit(QLineEdit):

    transfertRegistreAndChamps = pyqtSignal(object, object)
    transfertPositionStack = pyqtSignal(object)

    def __init__(self, champs, cdc):
        super().__init__()

        self.champs = champs
        self.cdc = cdc
        self.app_state = AppState() #instance global singleton

        self.setStyleSheet(
            """
            QLineEdit {
                font-family: 'Papyrus';
                font-size: 25px;
                border: 2px solid #2980b9;
                border-radius: 5px;
                padding: 5px;
            }
            """
        )

        self.setObjectName(self.champs.name_champs if self.champs is not None else "type_registre")

        #on met a jour le contenu du champs numero acte
        if self.objectName() == 'numero_acte':
            # self.app_state.numero_acte += 1
            self.setText(str(self.app_state.numero_acte))
        
        self.returnPressed.connect(self.okPressed)

    def event(self,event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.tabFollow()
            return True
        else:
            return QLineEdit.event(self,event)
          
    def tabFollow(self):
        if self.app_state.count_stack > self.app_state.next_position:
            self.app_state.next_position += 1
        self.transfertPositionStack.emit(self.app_state.next_position)
    
    def okPressed(self):
        if self.champs is None:
            dialog = DialogTableWidgetRegistre(self.cdc)
            dialog.selectTypeRegistreAndFieldsLinks.connect(self.onSelectTypeRegistreAndFieldsLinks)
            dialog.exec_()
        if 'lieu_' in self.objectName():
            dialog = DialogBaseVille(self.text())
            dialog.textRowSelected.connect(self.onSetLieuEvenement)
            dialog.exec_()



    def onSelectTypeRegistreAndFieldsLinks(self, registre, champs):
        self.setText(registre.type_registre)

        self.transfertRegistreAndChamps.emit(registre, champs)

    def onSetLieuEvenement(self, ville, departement):
        value = ville
        if departement != "":
            value = f"{ville} ({departement})"
        self.setText(value)
    