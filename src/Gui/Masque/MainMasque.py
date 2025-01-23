import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QMessageBox, QProgressBar, QLineEdit, QTableWidget
from PyQt5.QtGui import QKeyEvent
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
from src.Gui.Masque.DialogExportation import DialogExportation
from src.Gui.Widget.ContainerLineEdit import ContainerLineEdit

from src.Model.Registre import Registre
from src.Model.Champs import Champs
from src.Model.Production import Production

from src.Singleton.AppState import AppState
from datetime import datetime
from src.Date.DateTimeManager import DateTimeManager
from src.Repository.ProductionRepository import ProductionRepository
#pour le test
# from TiffViewer import TiffViewer
# from TableWidgetFilename import TableWidgetFilename

# Constantes pour les facteurs de zoom et le défilement
ZOOM_FACTOR_IN = 1.1
ZOOM_FACTOR_OUT = 0.9
SCROLL_STEP = 50  # Nombre de pixels pour le défilement

class MasqueWindow(QMainWindow):
    """
    Fenêtre principale de l'application de masquage.
    Permet la visualisation et le traitement des images de registres.
    """
    def __init__(self, user):
        """
        Initialise la fenêtre principale.
        
        Args:
            user: L'utilisateur connecté à l'application
        """
        super().__init__()
        # Charger le fichier .ui
        loadUi("src/Gui/Masque/MainMasque.ui", self)
        
        self.user = user

        self.registre_selected = None
        self.champs_selected = list()
        
        screen = QApplication.primaryScreen()

        self.app_state = AppState()

        self.list_images = list()
        self.images_path = "images"
        self.cdc_selected = None
        self.annee_registre = None
        # self.numero_acte = 0
        self.list_champs = list()
        self.current_index_image = 0

        self.data = list()
        self.data_previous_or_next_acte = {}
        
        self.dialog_widget_chargement = None

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
        self.table_widget_production.hide()
        self.progress_bar.hide()

        #tableau widget qui contient la liste des nom d'images à saisir
        self.table_widget_file_name = TableWidgetFilename()
        self.table_widget_file_name.hide()
        self.table_widget_file_name.setEditTriggers(QTableWidget.NoEditTriggers)
        #signal liste image cliquer
        self.table_widget_file_name.cellDoubleClicked.connect(self.onCellTableWidgetClicked)
        
        #masquer le menu administration
        if user.roles.type == "user":
            self.menuAdmin.menuAction().setVisible(False)

        #action signal
        self.action_chargement.triggered.connect(self.onOpenDialogChargement)
        self.action_gestion_roles.triggered.connect(self.onOpenDialogRoles)
        self.action_gestion_utilisateur.triggered.connect(self.onOpenDialogUser)
        self.action_gestion_champs.triggered.connect(self.onOpenDialogChamps)
        self.action_gestion_type_champs.triggered.connect(self.onOpenDialogTypeChamps)
        self.action_intervertir_les_champs.triggered.connect(self.onOpenDialogIntervertirChamps)

        self.action_exporter.triggered.connect(self.onOpenDialogExportation)

        self.showMaximized()

        # self.stacked_widget_champs.setFocus()

    def onOpenDialogChargement(self):
        self.dialog_widget_chargement = DialogChargement()
        self.dialog_widget_chargement.handleAnneePathImage.connect(self.onHandleAnneePathImage)
        self.dialog_widget_chargement.exec_()
    
    #chargement des images dans le stack_widget_champs
    def onHandleAnneePathImage(self, annee, path_image, cdc_select):
        
        self.annee_registre = annee
        self.cdc_selected = cdc_select
        
        self.appendChampsInstackChamps()
        self.appendImageInStackImage(path_image)
    
    
    def onGetChampsSelectedByRegistre(self, registre, champs):
        self.registre_selected = registre
        self.champs_selected = champs
        """ à chaque changement de type de registre valider, on enleve tous les champs dans le stack,
            puis on reinitisalise de tous le debut
        """
        if self.registre_selected != registre and self.registre_selected is not None:
            self.clearStackWidgetChamps()
            # self.initRegistreByCdc()
        """ et après, si après on ajoute le nouveau champs"""
        self.appendChampsInstackChamps()

    def clearStackWidgetChamps(self):
        """
        Nettoie tous les widgets du stack de champs.
        Assure une libération correcte de la mémoire.
        """
        while self.stacked_widget_champs.count() > 0:
            widget = self.stacked_widget_champs.widget(0)
            self.stacked_widget_champs.removeWidget(widget)
            widget.setParent(None)  
            widget.deleteLater()

    def appendChampsInstackChamps(self):
        """
        Ajoute les champs de saisie dans le stack widget.
        Crée et configure les conteneurs de champs avec leurs signaux.
        """
        type_registre = self.stacked_widget_champs.findChild(QLineEdit, 'type_registre')
        
        if type_registre is None:
            # Premier champ - création du conteneur initial
            container_line_edit = ContainerLineEdit(self.cdc_selected)
            self._connectContainerSignals(container_line_edit)
            container_line_edit.childrenFindRegistreAndChamps.connect(self.onGetChampsSelectedByRegistre)
            self.stacked_widget_champs.addWidget(container_line_edit)
            container_line_edit.setFocus()
        else:
            # Ajout des champs supplémentaires
            for champs in self.champs_selected:
                self.list_champs.append(champs.name_champs)
                container_line_edit = ContainerLineEdit(self.cdc_selected, champs)
                self._connectContainerSignals(container_line_edit)
                self.stacked_widget_champs.addWidget(container_line_edit)

        """singleton"""
        self.app_state.count_stack = self.stacked_widget_champs.count()
        
    def moveScrollBar(self, arrow_pressed, step):
        graphic_view = self.stacked_widget_images.currentWidget()
        
        if isinstance(graphic_view, QGraphicsView):
            match arrow_pressed:
                case 'up':
                    graphic_view.verticalScrollBar().setValue(graphic_view.verticalScrollBar().value() - SCROLL_STEP)
                case 'down':
                    graphic_view.verticalScrollBar().setValue(graphic_view.verticalScrollBar().value() + SCROLL_STEP)
                case 'left':
                    graphic_view.horizontalScrollBar().setValue(graphic_view.horizontalScrollBar().value() - SCROLL_STEP)
                case 'right':
                    graphic_view.horizontalScrollBar().setValue(graphic_view.horizontalScrollBar().value() + SCROLL_STEP)

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
                message["message"] = "Année de registre est differente de l'année d'évènement" if not 'date_dre' in name_widget else "Année de registre est différente de l'année du dressé"
        if 'heure' in name_widget:
            if not DateTimeManager.isTimeValid(date_or_time):
                message["is_valid"] = False
                message["message"] = "Heure est invalid"
        return message
    
    def onPreviousFieldInStack(self, previous_position):
        if previous_position < 0:
            self.app_state.current_position_line_edit = 0
            QMessageBox.information(self, "Information", "Il n'y a plus de champs")
            return
        self.stacked_widget_champs.setCurrentIndex(previous_position)

    def onNextFieldInStack(self, current_position_line_edit):
        """
        Gère le passage au champ suivant.
        Sauvegarde les données si tous les champs sont remplis.
        
        Args:
            current_position_line_edit: Position actuelle dans le stack
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
            # line_edit.setText(content)

            #verification date et heure
            info = self.checkDateOrTime(name, content)
            if not info['is_valid']:
                if "Année de registre" in info['message']:
                    reply = QMessageBox.question(self, 'Question', f"{info['message']}\nvoulez-vous continuer?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if reply == QMessageBox.No:
                        return
                else:
                    QMessageBox.critical(self, "Erreur", info['message'])
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

        self.app_state.current_position_line_edit = current_position_line_edit + 1
        self.stacked_widget_champs.setCurrentIndex(self.app_state.current_position_line_edit) # passer au champ suivant

        if self.app_state.current_position_line_edit == self.stacked_widget_champs.count():
            #Question sur l'enregistrement dans la base
            reply = QMessageBox.question(
                self,
                "Question",
                "Voulez-vous enregistrer ?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )

            if reply == QMessageBox.Yes:
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
                
                self.app_state.numero_acte += 1 # incrementation du numéro d'acte
                self.data = list()#reinitialisation la list

                reply = QMessageBox.question(
                    self,
                    "Question",
                    "Voulez-vous passer au image suivant?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.Yes
                )
                
                #chargement de l'image suivant
                if reply == QMessageBox.Yes:
                    if self.current_index_image < len(self.list_images):
                        self.current_index_image = self.current_index_image + 1

                        self.clearStackWidgetChamps()
                        self.appendChampsInstackChamps()
                        self.nextOrPreviousImage() #image suivant
                        self.table_widget_file_name.changeCurrentItem(self.current_index_image) #mettre en subrillance l'item suivant

                self.app_state.count_stack = 0
                self.app_state.current_position_line_edit = 0
                    

                # elif reply == QMessageBox.No:
                #     return
                    # self.clearStackWidgetChamps()
                    # self.initRegistreByCdc()
                    # self.nextOrPreviousImage() #image suivant
                    # self.app_state.current_position_line_edit = 0
                    # self.app_state.count_stack = 0

                # if reply == QMessageBox.No:
                #     return

    def appendImageInStackImage(self, path):
        """
        Charge récursivement les images depuis le chemin spécifié.
        
        Args:
            path: Chemin du dossier contenant les images
            
        Gère les erreurs de chargement des fichiers.
        """
        try:
            for i, file in enumerate(os.scandir(path)):
                if file.is_file():
                    graphic_viewer = TiffViewer(path+"/"+file.name)
                    self.stacked_widget_images.addWidget(graphic_viewer)
                    self.list_images.append(file.name)
                    """mise a jour de la progress bar"""
                    self.dialog_widget_chargement.progressBar.setValue(round(i*100/self.dialog_widget_chargement.total_files))
                else:
                    self.appendImageInStackImage(path+"/"+file.name)
        except OSError as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement des images: {str(e)}")
        #après le scan, on met a jour le table widget qui contient les nom de fichier
        self.table_widget_file_name.appendRow(self.list_images)
        self.scroll_area_list_images.setWidget(self.table_widget_file_name)

        #on affiche le progress bar et le scroll area list
        self.progress_bar.show()
        self.scroll_area_list_images.show()
        self.table_widget_production.show()

    def keyPressEvent(self, event: QKeyEvent):
        """
        Gère les événements clavier pour la navigation et le zoom.
        
        Args:
            event: L'événement clavier reçu
        """
        key = event.text()
        modifiers = event.modifiers()
        #image suivant
        if event.key() == Qt.Key_F7:
            if self.stacked_widget_images.currentIndex() == self.stacked_widget_images.count() - 1:
                QMessageBox.information(None, "Erreur", "Il n'y a plus d'image")
                return
            self.nextOrPreviousImage()
            self.table_widget_file_name.changeCurrentItem(self.stacked_widget_images.currentIndex())
        #image précedent
        elif event.key() == Qt.Key_F3:
            if self.stacked_widget_images.currentIndex() == 0:
                QMessageBox.information(None, "Erreur", "Il n'y a plus d'image")
                return
            else:
                self.app_state.numero_acte -= 1
                self.nextOrPreviousImage(False)
                self.table_widget_file_name.changeCurrentItem(self.stacked_widget_images.currentIndex())

                production_repository = ProductionRepository()
                data_previous_acte = production_repository.findDataPreviousActe(self.cdc_selected, self.registre_selected, self.user, self.annee_registre)

                #reinitialiser des widgets
                self.clearStackWidgetChamps()
                # self.initRegistreByCdc()
                # self.appendChampsInstackChamps()
                self.presetDataPreviousActe(data_previous_acte)
                self.app_state.count_stack = 0
                self.app_state.current_position_line_edit = 0
            
        #zoom images
        if event.modifiers() & Qt.ControlModifier:
            if event.key() == Qt.Key_Plus or event.key() == Qt.Key_Equal:  # "+" peut être aussi "=" sur certains claviers
                self.zoom()
            elif event.key() == Qt.Key_Minus:
                self.zoom(False)

    def presetDataPreviousActe(self, productions):
        for production in productions:
            pass
        # for production in productions:
        #     print(f"valeur => {production.valeur_champ} name_champs=> {production.champs.name_champs}")
        # for champs in self.champs_selected:
        #         self.list_champs.append(champs.name_champs)
        #         container_line_edit = ContainerLineEdit(self.cdc_selected, champs)
        #         """signal personnalisé"""
        #         container_line_edit.nextPositionInStack.connect(self.onNextFieldInStack)
        #         container_line_edit.previousPositionInStack.connect(self.onPreviousFieldInStack) 
        #         container_line_edit.zoom.connect(self.zoom)
        #         container_line_edit.scrollDefile.connect(self.moveScrollBar)

        #         self.stacked_widget_champs.addWidget(container_line_edit)


    def nextOrPreviousImage(self, is_next_image = True):
        self.stacked_widget_images.setCurrentIndex(self.stacked_widget_images.currentIndex() + 1 if is_next_image else self.stacked_widget_images.currentIndex() - 1)
        self.stacked_widget_images.setCurrentWidget(self.stacked_widget_images.widget(self.stacked_widget_images.currentIndex()))

    def selectRowTableWidgetFileName(self):
        pass
          
    def zoom(self, is_zoom_plus):
            graphic_viewer = self.stacked_widget_images.currentWidget()
            if is_zoom_plus:
                graphic_viewer.scale(ZOOM_FACTOR_IN, ZOOM_FACTOR_IN)  # Zoom avant
            else:
                graphic_viewer.scale(ZOOM_FACTOR_OUT, ZOOM_FACTOR_OUT)  # Zoom avant

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

    def onOpenDialogExportation(self):
        dialog_exportation = DialogExportation()
        dialog_exportation.exec_()

    def _connectContainerSignals(self, container):
        """
        Configure les connexions des signaux pour un conteneur de champs.
        
        Args:
            container: Le conteneur de champs à configurer
        """
        container.nextPositionInStack.connect(self.onNextFieldInStack)
        container.previousPositionInStack.connect(self.onPreviousFieldInStack)
        container.zoom.connect(self.zoom)
        container.scrollDefile.connect(self.moveScrollBar)


        

# if __name__ == "__main__":
    
# app = QApplication(sys.argv)
# window = MasqueWindow()
# window.show()

# sys.exit(app.exec_())