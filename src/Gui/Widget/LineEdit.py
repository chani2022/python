import re
from PyQt5.QtWidgets import QLineEdit, QMessageBox
from PyQt5.QtCore import Qt, QEvent, pyqtSignal
from src.Gui.Masque.DialogTableWidgetTypeActe import DialogTableWidgetTypeActe
from src.Singleton.AppState import AppState
from src.Gui.BaseVille.DialogBaseVille import DialogBaseVille
from src.Repository.PrenomRepository import PrenomRepository
from src.Gui.MessageBox.MessageBox import MessageBox

class LineEdit(QLineEdit):

    tabPressed = pyqtSignal()
    escapePressed = pyqtSignal()
    ctrlPressed = pyqtSignal(object)
    ctrlDirectionPressed = pyqtSignal(object, object)

    def __init__(self, champs, famille, numero_acte):
        super().__init__()

        self.champs = champs
        self.numero_acte = numero_acte
        self.famille = famille
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

        self.setObjectName(self.champs.name_champs)

        #on met a jour le contenu du champs numero acte
        if self.objectName() == 'numero_acte':
            # self.app_state.numero_acte += 1
            self.setText(str(self.numero_acte))
        
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
            """
            key release evenement classique
            SEULEMENT POUR LE CDC LOG(logitude)
            """
            match self.famille.cdc.nom_cdc:
                case 'LOG':
                    if event.type() == QEvent.KeyRelease:
                        name_object = self.objectName()
                        content = self.text()
                        if re.search(r'prenom', name_object):
                            pass
                        elif re.search(r'nom', name_object):
                            """
                            TOUS EN MAJUSCULE DAN LE CHAMP
                            """
                            self.setText(content.upper())
                        elif re.search(r'numero', name_object):
                            if re.search(r"_acte",name_object):
                                self.setText(content.upper())


            return QLineEdit.event(self,event)
        
    def ctrlDirectionFollow(self, arrow_pressed):
        step = 40
        self.ctrlDirectionPressed.emit(arrow_pressed, step)
    #zoom
    def ctrlFollow(self, is_zoom_plus):
        self.ctrlPressed.emit(is_zoom_plus)
    #champs suivant
    def tabFollow(self):
        self.tabPressed.emit()

    def EscapeFollow(self):
        self.escapePressed.emit()

    #choix sur les boite de dialogue
    def okPressed(self):
        """famille dialog"""
        match self.famille.cdc.nom_cdc:
            case 'LOG':
                if re.search(r'type_', self.objectName()):
                    dialog = DialogTableWidgetTypeActe(self.famille)
                    dialog.getTypeActe.connect(self.onGetTypeActeSelected)
                    dialog.exec_()
                if re.search(r'lieu_|ville_', self.objectName()):
                    dialog = DialogBaseVille(self.text())
                    dialog.returnPressed.connect(self.onVilleSelected)
                    dialog.exec_()

    def onGetTypeActeSelected(self, TypeActe):
        self.setText(TypeActe.valeur)

        # self.onGetTypeActe.emit(TypeActe)

    def onVilleSelected(self, ville, departement):
        value = ville
        if departement != "":
            value = f"{ville} ({departement})"
        self.setText(value)

    