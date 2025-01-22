from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt, QEvent, pyqtSignal
from src.Gui.Widget.DialogTableWidgetRegistre import DialogTableWidgetRegistre
from src.Singleton.AppState import AppState
from src.Gui.BaseVille.DialogBaseVille import DialogBaseVille

class LineEdit(QLineEdit):

    registreAndChampsSelected = pyqtSignal(object, object)
    tabPressed = pyqtSignal(object)
    EscapePressed = pyqtSignal(object)
    ctrlPressed = pyqtSignal(object)
    ctrlDirectionPressed = pyqtSignal(object, object)

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
        #champ suivant
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            # print(self.objectName())
            self.tabFollow()
            return True
        #champ precedent
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Escape:
            
            self.EscapeFollow()
            return True
        #zoom et defilement image
        elif event.type() == QEvent.KeyPress and event.modifiers() & Qt.ControlModifier:
            #zoom
            if event.key() == Qt.Key_Plus or event.key() == Qt.Key_Equal:  # "+" peut être aussi "=" sur certains claviers
                self.ctrlFollow(True)
            elif event.key() == Qt.Key_Minus:
                self.ctrlFollow(False)
            #defilement image scrollArea
            elif event.key() == Qt.Key_Up:
                self.ctrlDirectionFollow("up")
            elif event.key() == Qt.Key_Down:
                self.ctrlDirectionFollow("down")
            elif event.key() == Qt.Key_Left:
                self.ctrlDirectionFollow("left")    
            elif event.key() == Qt.Key_Right:
                self.ctrlDirectionFollow("right")
            return True
        else:
            return QLineEdit.event(self,event)
        
    def ctrlDirectionFollow(self, arrow_pressed):
        step = 40
        self.ctrlDirectionPressed.emit(arrow_pressed, step)
    #zoom
    def ctrlFollow(self, is_zoom_plus):
        self.ctrlPressed.emit(is_zoom_plus)
    #champs suivant
    def tabFollow(self):
        # if self.app_state.count_stack > self.app_state.current_position_line_edit:
        #     self.app_state.current_position_line_edit += 1

        self.tabPressed.emit(self.app_state.current_position_line_edit)

    def EscapeFollow(self):
        if self.app_state.current_position_line_edit >= 0:
            self.app_state.current_position_line_edit -= 1

        self.EscapePressed.emit(self.app_state.current_position_line_edit)

    #choix sur les boite de dialogue
    def okPressed(self):
        if self.champs is None:
            dialog = DialogTableWidgetRegistre(self.cdc)
            dialog.returnPressed.connect(self.onRegistreChampsSelected)
            dialog.exec_()
        if 'lieu_' in self.objectName():
            dialog = DialogBaseVille(self.text())
            dialog.returnPressed.connect(self.onVilleSelected)
            dialog.exec_()



    def onRegistreChampsSelected(self, registre, champs):
        self.setText(registre.type_registre)

        self.registreAndChampsSelected.emit(registre, champs)

    def onVilleSelected(self, ville, departement):
        value = ville
        if departement != "":
            value = f"{ville} ({departement})"
        self.setText(value)
    