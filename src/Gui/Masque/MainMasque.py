import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QMessageBox, QProgressBar, QGroupBox, QTableWidget, QVBoxLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QKeyEvent, QFont
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
import os
from distutils.dir_util import copy_tree
#pour la generalité
from src.Gui.Masque.TiffViewer import TiffViewer
from src.Gui.Masque.TableWidgetFilename import TableWidgetFilename
from src.Gui.Admin.DialogRoles import DialogRoles
from src.Gui.Admin.DialogUser import DialogUser
from src.Gui.Admin.DialogCdcRegistre import DialogCdcRegistre
from src.Gui.Admin.DialogTypeChamps import DialogTypeChamps
from src.Gui.Masque.DialogIntervertirChamps import DialogIntervertirChamps
from src.Gui.Masque.DialogChargement import DialogChargement
from src.Gui.Widget.ContainerLineEdit import ContainerLineEdit

from src.Model.Registre import Registre
from src.Model.Champs import Champs
from src.Model.Production import Production

from src.Singleton.AppState import AppState
from datetime import datetime
from src.Date.DateTimeManager import DateTimeManager
#pour le test
# from TiffViewer import TiffViewer
# from TableWidgetFilename import TableWidgetFilename


class MasqueWindow(QMainWindow):
    #pour la generalité
    def __init__(self, user):
    #pour le test
    # def __init__(self):
        super().__init__()
        # Charger le fichier .ui
        loadUi("src/Gui/Masque/MainMasque.ui", self)
        
        self.user = user

        self.registre_selected = None
        self.champs_selected = None
        
        screen = QApplication.primaryScreen()

        self.app_state = AppState()

        self.list_images = list()
        self.images_path = "images"
        self.cdc_selected = None
        self.annee_registre = None
        # self.numero_acte = 0
        self.list_champs = list()

        self.data = list()

        #repositionner le splitter central
        taille_ecran = screen.geometry()
        height_stack_up = taille_ecran.height() - 75
        height_stack_down = taille_ecran.height() - height_stack_up
        self.splitter_center.setSizes([height_stack_up, height_stack_down])

        #progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100) 
        self.progress_bar.setMinimum(0)   
        self.progress_bar.setValue(0)     
        self.progress_bar.setTextVisible(True)
        self.status_bar.addWidget(self.progress_bar)

        #on cache par defaut le scroll area image, progressbar
        self.scroll_area_list_images.hide()
        self.progress_bar.hide()

        #tableau widget qui contient la liste des nom d'images à saisir
        self.table_widget_file_name = TableWidgetFilename()
        self.table_widget_file_name.hide()
        self.table_widget_file_name.setEditTriggers(QTableWidget.NoEditTriggers)
        #signal liste image cliquer
        self.table_widget_file_name.cellDoubleClicked.connect(self.onCellTableWidgetClicked)
        
        if user.roles.type == "user":
            self.action_gestion_roles.setVisible(False)
            self.action_gestion_utilisateur.setVisible(False)
        #action signal
        self.action_chargement.triggered.connect(self.onOpenDialogChargement)
        self.action_gestion_roles.triggered.connect(self.onOpenDialogRoles)
        self.action_gestion_utilisateur.triggered.connect(self.onOpenDialogUser)
        self.action_gestion_champs.triggered.connect(self.onOpenDialogChamps)
        self.action_gestion_type_champs.triggered.connect(self.onOpenDialogTypeChamps)
        self.action_intervertir_les_champs.triggered.connect(self.onOpenDialogIntervertirChamps)

        self.showMaximized()

        # self.stacked_widget_champs.setFocus()

    def onOpenDialogChargement(self):
        dialog_widget_chargement = DialogChargement()
        dialog_widget_chargement.handleAnneePathImage.connect(self.onHandleAnneePathImage)
        dialog_widget_chargement.exec_()
    
    #chargement des images dans le stack_widget_champs
    def onHandleAnneePathImage(self, annee, path_image, cdc_select):
        self.appendImageInStackImage(path_image)
        self.annee_registre = annee
        self.cdc_selected = cdc_select
        
        # self.data["cdc"] = cdc_select

        self.initRegistreByCdc()

    def initRegistreByCdc(self):
        
        input_registre = ContainerLineEdit(self.cdc_selected)
        input_registre.transfertRegistreAndChamps.connect(self.onGetChampsSelectedByRegistre)#signal personnalisé
        input_registre.nextPositionInStack.connect(self.onNextFieldInStack)
        self.stacked_widget_champs.addWidget(input_registre)
        input_registre.setFocus()
    
    
    def onGetChampsSelectedByRegistre(self, registre, champs):
        self.registre_selected = registre
        self.champs_selected = champs
        """ à chaque changement de type de registre valider, on enleve tous les champs dans le stack,
            puis on reinitisalise de tous le debut
        """
        if self.registre_selected != registre and self.registre_selected is not None:
            self.clearStackWidgetChamps()
            self.initRegistreByCdc()
        """ et après, si après on ajoute le nouveau champs"""
        self.appendChampsInstackChamps()

    def clearStackWidgetChamps(self):
        while self.stacked_widget_champs.count() > 0:
            widget = self.stacked_widget_champs.widget(0)  # Obtenez le premier widget
            self.stacked_widget_champs.removeWidget(widget)  # Retirez le widget du QStackedWidget
            widget.deleteLater()  # Détruisez le widget pour libérer la mémoire

    def appendChampsInstackChamps(self):
        for champs in self.champs_selected:
            # print(champs.label_champ)
            self.list_champs.append(champs.name_champs)
            input = ContainerLineEdit(self.cdc_selected, champs)
            # input.transfertRegistreAndChamps.connect(self.onGetChampsSelectedByRegistre)#signal personnalisé
            input.nextPositionInStack.connect(self.onNextFieldInStack)

            self.stacked_widget_champs.addWidget(input)
            """singleton"""
            # app_state = AppState()  # Accéder à l'instance unique
            self.app_state.count_stack = self.stacked_widget_champs.count()

    def checkDateOrTime(self, name_widget, date_or_time):
        # is_valid = True
        message = {
            "is_valid": True,
            "message": None
        }
        if 'date' in name_widget:
            if not DateTimeManager.isDateValid(date_or_time):
                # QMessageBox.critical(self, "Erreur", "La date est invalid")
                message["is_valid"] = False
                message["message"] = "La date est invalid"
                return message
            
            annee = date_or_time[-4:]
            if annee != self.annee_registre:
                # QMessageBox.critical(self, "Erreur", "La date de registre est differente de la date d'évènement")
                message["is_valid"] = False
                message["message"] = "La date de registre est differente de la date d'évènement"
        if 'heure' in name_widget:
            if not DateTimeManager.isTimeValid(date_or_time):
                
                message["is_valid"] = False
                message["message"] = "Heure est invalid"
        return message

    def onNextFieldInStack(self, next_position):
        """ avant de changer la prochaine widget, on recuper les information
            du page précedent
        """
        data = [ 
            self.cdc_selected, 
            self.registre_selected, 
            self.user,
            datetime.now(),
            self.annee_registre
        ]
        line_edit = self.stacked_widget_champs.currentWidget().findChild(QLineEdit)
        if line_edit:
            name = line_edit.objectName()
            content = line_edit.text()
            if name == 'numero_acte':
                self.app_state.numero_acte = int(content)
            if 'nom' in name:
                content = content.upper()
            if 'prenom' in name:
                content = content.title()

            #verification date et heure
            info = self.checkDateOrTime(name, content)
            if not info["is_valid"]:
                QMessageBox.critical(self, "Erreur", info["message"])
                return

            champ = None
            for name_champ in self.list_champs:
                if name_champ == name:
                    champ = Champs.select().where((Champs.registre == self.registre_selected) & (Champs.name_champs == name_champ)).get()
                

            data.append(content)
            data.append(self.app_state.numero_acte)
            data.append(champ)
            
            current_index_image = self.stacked_widget_images.currentIndex()
            data.append(self.list_images[current_index_image])

        self.data.append(tuple(data))

        self.stacked_widget_champs.setCurrentIndex(next_position) # passer au champ suivant

        if next_position == self.stacked_widget_champs.count():
            reply = QMessageBox.question(
                self,
                "Question",
                "Voulez-vous enregistrer ?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                QMessageBox.Yes
            )

            # Vérifier la réponse
            if reply == QMessageBox.Yes:
                print("L'utilisateur a cliqué sur Oui")
                #enregistrement dans la base
                Production.insert_many(
                    self.data, 
                    fields=[
                        Production.cdc, 
                        Production.registre, 
                        Production.user, 
                        Production.date_traitement,
                        Production.annee_registre,
                        Production.valeur_champ, 
                        Production.numero_acte,
                        Production.champs,
                        Production.nom_image,
                        
                ]).execute()

                self.data = list()#puis on reinitialise la list
                """placer dans l'enregistrement, mais pas dans l'acte suivant,
                    car une image peut contenir plusieur images
                """
                self.app_state.numero_acte +=1

                reply = QMessageBox.question(
                    self,
                    "Question",
                    "Voulez-vous passer au image suivant?",
                    QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                    QMessageBox.Yes
                )
                #chargement de l'image suivant
                if reply == QMessageBox.Yes:
                    self.clearStackWidgetChamps()
                    self.initRegistreByCdc()
                    self.imageManipilator() #image suivant
                    self.app_state.next_position = 0
                    self.app_state.count_stack = 0
                    pass

            elif reply == QMessageBox.No:
                return
            else:
                return

    def appendImageInStackImage(self, path):
        for i, file in enumerate(os.scandir(path)):
            if file.is_file():
                scroll_area = TiffViewer(path+"/"+file.name)
                self.stacked_widget_images.addWidget(scroll_area)
                self.list_images.append(file.name)
            else:
                self.appendImageInStackImage(path+"/"+file.name)
        #après le scan, on met a jour le table widget
        self.table_widget_file_name.appendRow(self.list_images)
        self.scroll_area_list_images.setWidget(self.table_widget_file_name)

        #on affiche le progress bar et le scroll area list
        self.progress_bar.show()
        self.scroll_area_list_images.show()

    def keyPressEvent(self, event: QKeyEvent):
        """Méthode appelée lorsqu'une touche est pressée."""
        key = event.text()
        modifiers = event.modifiers()
        #image suivant
        if event.key() == Qt.Key_F7:
            if self.stacked_widget_images.currentIndex() == self.stacked_widget_images.count() - 1:
                QMessageBox.information(None, "Erreur", "Il n'y a plus d'image")
                return
            self.imageManipilator()
            self.table_widget_file_name.changeCurrentItem(self.stacked_widget_images.currentIndex())
        #image précedent
        elif event.key() == Qt.Key_F3:
            if self.stacked_widget_images.currentIndex() == 0:
                QMessageBox.information(None, "Erreur", "Il n'y a plus d'image")
                return
            self.imageManipilator(False)
            self.table_widget_file_name.changeCurrentItem(self.stacked_widget_images.currentIndex())
            
        #zoom images
        if event.modifiers() & Qt.ControlModifier:
            if event.key() == Qt.Key_Plus or event.key() == Qt.Key_Equal:  # "+" peut être aussi "=" sur certains claviers
                self.scaleImage()
            elif event.key() == Qt.Key_Minus:
                self.scaleImage(False)

    def imageManipilator(self, is_next_image = True):
        if is_next_image:
            self.stacked_widget_images.setCurrentIndex(self.stacked_widget_images.currentIndex() + 1)
            self.stacked_widget_images.setCurrentWidget(self.stacked_widget_images.widget(self.stacked_widget_images.currentIndex()))
        else:
            self.stacked_widget_images.setCurrentIndex(self.stacked_widget_images.currentIndex() - 1)
            self.stacked_widget_images.setCurrentWidget(self.stacked_widget_images.widget(self.stacked_widget_images.currentIndex()))
        
    def scaleImage(self, is_zoom_plus = True):
            scroll_area = self.stacked_widget_images.widget(self.stacked_widget_images.currentIndex())
            label = scroll_area.widget()
            
            pixmap = label.pixmap()
            width_pixmap = pixmap.size().width()
            height_pixmap = pixmap.size().height()
            if is_zoom_plus:
                width_pixmap += 40
                height_pixmap += 40
            else:
                width_pixmap -= 40
                height_pixmap -= 40

            image_scaled = pixmap.scaled(
                    width_pixmap, height_pixmap, 
                    Qt.KeepAspectRatio,  # Conserver le ratio de l'image
                    Qt.SmoothTransformation  # Transformation lisse pour une meilleure qualité
                    # Qt.FastTransformation
                )
            #mise a jour de la taille de l'image
            label.setPixmap(image_scaled)
            # label.setScaledContents(True)
            scroll_area.setWidget(label)
            self.stacked_widget_images.setCurrentWidget(scroll_area)

    def onCellTableWidgetClicked(self, row, column):
        self.stacked_widget_images.setCurrentIndex(row)
        self.stacked_widget_images.setCurrentWidget(self.stacked_widget_images.widget(row))

    def onOpenDialogRoles(self):
        dialog_widget_roles = DialogRoles()
        dialog_widget_roles.exec_()

    def onOpenDialogUser(self):
        dialog_widget_user = DialogUser()
        dialog_widget_user.exec_()
        pass
        # pass
    def onOpenDialogChamps(self):
        dialog_widget_champs = DialogCdcRegistre()
        dialog_widget_champs.exec_()

    def onOpenDialogTypeChamps(self):
        dialog_widget_type_champs = DialogTypeChamps()
        dialog_widget_type_champs.exec_()

    def onOpenDialogIntervertirChamps(self):
        dialog_widget_intervertir_champs = DialogIntervertirChamps()
        dialog_widget_intervertir_champs.exec_()


        

# if __name__ == "__main__":
    
# app = QApplication(sys.argv)
# window = MasqueWindow()
# window.show()

# sys.exit(app.exec_())