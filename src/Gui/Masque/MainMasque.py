import sys
import math
import os
import re
from datetime import datetime, time
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QMessageBox, QProgressBar, QLineEdit, QTableWidget, QTableWidgetItem
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
from src.Gui.Admin.DialogCdcFamille import DialogCdcFamille
from src.Gui.Admin.DialogTypeChamps import DialogTypeChamps
from src.Gui.Masque.DialogIntervertirChamps import DialogIntervertirChamps
from src.Gui.Masque.DialogChargement import DialogChargement
from src.Gui.Masque.DialogExportation import DialogExportation
from src.Gui.Widget.ContainerLineEdit import ContainerLineEdit

from src.Model.TypeActe import TypeActe
from src.Model.Champs import Champs
from src.Model.Famille import Famille

from datetime import datetime
from src.Date.DateTimeManager import DateTimeManager
from src.Repository.NaissanceRepository import NaissanceRepository
from src.Validator.Validator import Validator
from src.Gui.MessageBox.MessageBox import MessageBox
from src.Date.DateTimeManager import DateTimeManager


#pour le test
# from TiffViewer import TiffViewer
# from TableWidgetFilename import TableWidgetFilename



class MasqueWindow(QMainWindow):

    # Constantes pour les facteurs de zoom et le défilement
    ZOOM_FACTOR_IN = 1.1
    ZOOM_FACTOR_OUT = 0.9
    SCROLL_STEP = 50  # Nombre de pixels pour le défilement

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

        self.data = {
            "user": self.user
        }

        # self.validator = None
        self.champs = list()
        
        screen = QApplication.primaryScreen()

        self.list_images = list()
        self.images_path = "images"
        self.numero_acte = 1
        # self.cdc_selected = None
        # self.annee_registre = None
        self.famille_selected = None
        self.is_1_file_many_acte = None
        # self.type_acte = None
        # self.numero_acte = 0
        self.list_champs = list()
        self.current_index_image = 0
        self.current_index_field = 0

        # self.data = list()
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
        self.progress_bar.hide()
        self.table_widget_production.hide()
        self.table_widget_production.setEditTriggers(QTableWidget.NoEditTriggers)  # Désactive l'édition pour tout le tableau

        #tableau widget qui contient la liste des nom d'images à saisir
        self.table_widget_file_name = TableWidgetFilename()
        self.table_widget_file_name.hide()
        self.table_widget_file_name.setEditTriggers(QTableWidget.NoEditTriggers)
        #signal liste image cliquer
        self.table_widget_file_name.cellDoubleClicked.connect(self.onCellDoubleClickedTableFileName)
        
        #masquer le menu administration
        if user.roles.type == "user":
            self.menuAdmin.menuAction().setVisible(False)

        #action signal
        self.action_chargement.triggered.connect(self.onOpenDialogChargement)
        self.action_gestion_roles.triggered.connect(self.onOpenDialogRoles)
        self.action_gestion_utilisateur.triggered.connect(self.onOpenDialogUser)
        self.action_gestion_champs.triggered.connect(self.onOpenDialogChamps)
        self.action_intervertir_les_champs.triggered.connect(self.onOpenDialogIntervertirChamps)

        self.action_exporter.triggered.connect(self.onOpenDialogExportation)

        self.showMaximized()


    def onOpenDialogChargement(self):
        self.dialog_widget_chargement = DialogChargement()
        self.dialog_widget_chargement.handleAnneePathImage.connect(self.onLoadImagesAndFieldsInStackWidget)
        self.dialog_widget_chargement.exec_()
    
    #chargement des champs et image et mise a jour table widget production dans le stack_widget_images
    def onLoadImagesAndFieldsInStackWidget(self, numero_registre: str, path_image: str, Famille_selected: object, is_1_file_many_acte: bool):

        self.famille_selected = Famille_selected
        self.is_1_file_many_acte = is_1_file_many_acte

        self.champs = Champs.select().where(Champs.famille == Famille_selected).order_by(Champs.position)
        familles = Famille.select().where(Famille.cdc == Famille_selected.cdc)
    
        nom_cdc_current = Famille_selected.cdc.nom_cdc
        self.preLoadData(nom_cdc_current, familles, numero_registre)
    
        self.appendChampsInstackChamps()
        self.appendImageInStackImage(path_image)
        """
        charger les 10 derniers lignes
        et modification du progressbar
        """
        self.updateTableWidgetProduction()
        self.setValueProgressBar()

    def preLoadData(self, nom_cdc_current:str, familles:list, numero_registre: str):

        # familles = Famille.select().where(Famille.cdc == Famille_selected.cdc)
        # nom_cdc_current = Famille_selected.cdc.nom_cdc
        match nom_cdc_current:
            case 'LOG':
                """
                    POUR LE CDC LOG
                """
                self.data['numero_registre'] = numero_registre
                self.data['famille'] = self.famille_selected
                for famille in familles:
                    nom_famille = famille.nom_famille
                        # self.data["code_etat"] = 0
                    if re.search(r"NAISSANC|RECONNAISSANC", nom_famille):
                        if re.search(r"NAISSAN", nom_famille):
                            self.data['code_commune'] = 'A0'
                        self.data["code_famille_acte"] = 'N'
                        self.data["code_etat"] = 0

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
        for champs in self.champs:
            self.list_champs.append(champs.name_champs)
            container_line_edit = ContainerLineEdit(self.famille_selected, champs, self.numero_acte)
            self._connectContainerSignals(container_line_edit)
            self.stacked_widget_champs.addWidget(container_line_edit)
            container_line_edit.setFocus()

        """singleton"""
        self.app_state.count_stack = self.stacked_widget_champs.count()
        
    def moveScrollBar(self, arrow_pressed):
        graphic_view = self.stacked_widget_images.currentWidget()
        
        if isinstance(graphic_view, QGraphicsView):
            match arrow_pressed:
                case 'up':
                    graphic_view.verticalScrollBar().setValue(graphic_view.verticalScrollBar().value() - MasqueWindow.SCROLL_STEP)
                case 'down':
                    graphic_view.verticalScrollBar().setValue(graphic_view.verticalScrollBar().value() + MasqueWindow.SCROLL_STEP)
                case 'left':
                    graphic_view.horizontalScrollBar().setValue(graphic_view.horizontalScrollBar().value() - MasqueWindow.SCROLL_STEP)
                case 'right':
                    graphic_view.horizontalScrollBar().setValue(graphic_view.horizontalScrollBar().value() + MasqueWindow.SCROLL_STEP)
    
    def onPreviousFieldInStack(self):
        if self.current_index_field == 0:
            QMessageBox.information(self, "Information", "Il n'y a plus de champs")
            return
        
        self.current_index_field -= 1
        self.stacked_widget_champs.setCurrentIndex(self.current_index_field)

    def onNextFieldInStack(self):
        """
        Gère le passage au champ suivant.
        Sauvegarde les données si tous les champs sont valides.
        """
        line_edit = self.stacked_widget_champs.currentWidget().findChild(QLineEdit)
        if line_edit:
            name_widget = line_edit.objectName()
            content = line_edit.text()
            
            validator = Validator.validate(line_edit, self.champs, self.famille_selected, self.data)
            is_valid, message, content, type = validator.get('is_valid'), validator.get('message'), validator.get('value'), validator.get('type')

            if not is_valid:
                match type:
                    case 'critical':
                        MessageBox.show(type, message)
                        return
                    case 'question':
                        reply = MessageBox.show(type, message)
                        if reply == QMessageBox.No:
                            return
                    case 'castNumeroActeOk':
                        """
                        donc pas de string comme bis
                        """
                        self.numero_acte = content + 1
                    case 'castNumeroActeFailed':
                        self.numero_acte += 1
            
            """
            passage au champs suivant
            """
            self.current_index_field += 1
            self.stacked_widget_champs.setCurrentIndex(self.current_index_field)
            """
            mettre à jour le donnée à sauvegarder
            """
            self.data[name_widget] = content     
            """
            A la fin des champs,
            on fait une traitement
            """
            if self.current_index_field >= len(self.champs):
                reply = MessageBox.show('question', "Voulez vous enregistrer?")
                """
                sauvegarde ou modification des données
                """
                if reply == QMessageBox.Ok:
                    self.data['date_traitement'] = datetime.now()
                    self.data['heure_traitement'] = datetime.now().time()
                    self.data['nom_fichier'] = self.list_images[self.current_index_image]
                    """
                    informe l'utilisateur s'il veut mettre à jour l'acte
                    """
                    if self.acteExist(self.data["numero_acte"], self.data["numero_registre"]):
                        reply = MessageBox.show('question', f"L'acte N°{self.data['numero_acte']} existe déjà.\n Voulez-vous le modifier?")
                        if reply == QMessageBox.Ok:
                            acte = self.getOneActe(self.data['numero_acte'], self.data['numero_registre'])
                            self.updateData(acte.id)
                    else:
                        """
                        sauvegarde
                        """
                        self.saveData()
                        self.setValueProgressBar()
                        self.updateTableWidgetProduction()
                
                    reply = MessageBox.show('question', "Voulez vous passer au image suivant?")
                    if reply == QMessageBox.Ok:
                        self.nextImage()
                        self.setCurrentFileNameWidget()

                    elif reply == QMessageBox.No:
                        return
                    """
                    reinitialisation:
                        partiel du donnée
                        la vue stack widget champs
                        index du champs
                    """
                    self.initPartialData()
                    self.clearStackWidgetChamps()
                    self.appendChampsInstackChamps()
                    self.current_index_field = 0

                else:
                    self.current_index_field -= 1

    def initPartialData(self)->None:
        match self.famille_selected.cdc.nom_cdc:
            case 'LOG':
                """
                POUR LA COMPARAISON D'acte suivant
                a chaque nouvelle d'acte, on doit reinitiliser ces données
                """
                self.data['date_dresse'] = None
                self.data['date_evenement'] = None
                self.data['nom_pere'] = None
                self.data['nom_principal'] = None
            
    def saveData(self):
        match self.famille_selected.cdc.nom_cdc:
            case 'LOG':
                if re.search(r'NAISSAN', self.famille_selected.nom_famille):
                    NaissanceRepository.saveData(self.data)

    def updateData(self, id: int):
        match self.famille_selected.cdc.nom_cdc:
            case 'LOG':
                if re.search(r'NAISSAN', self.famille_selected.nom_famille):
                    NaissanceRepository.updateActe(self.data, id)

    def acteExist(self, numero_acte: int, numero_registre: int)->bool:
        exist = False
        match self.famille_selected.cdc.nom_cdc:
            case 'LOG':
                if re.search(r'NAISSAN', self.famille_selected.nom_famille):
                   exist =  NaissanceRepository.acteExist(self.famille_selected, numero_acte, numero_registre)

        return exist
    
    def getOneActe(self, numero_acte: str, numero_registre: int)-> any:
        acte = None
        match self.famille_selected.cdc.nom_cdc:
            case 'LOG':
                if re.search(r'NAISSAN', self.famille_selected.nom_famille):
                   acte =  NaissanceRepository.getOneActe(self.famille_selected, numero_acte, numero_registre)
        return acte

    def getCountRowActe(self)->int:
        count = None
        match self.famille_selected.cdc.nom_cdc:
            case 'LOG':
                if re.search(r'NAISSAN', self.famille_selected.nom_famille):
                   """
                   calculer la progression actuel
                   1fichier->4ligne
                             ?ligne
                   """
                   count_row = NaissanceRepository.count(self.famille_selected, self.data['numero_registre'])
                   count =  math.floor(count_row / 4) if self.is_1_file_many_acte else count_row
        return count
    
    def updateTableWidgetProduction(self):
        actes = list()
        match self.famille_selected.cdc.nom_cdc:
            case 'LOG':
                if re.search(r'^NAISSAN|^RECONNAIS', self.famille_selected.nom_famille):
                   actes = NaissanceRepository.getLastActes(self.famille_selected, self.data["numero_registre"])
                   self.table_widget_production.setRowCount(len(actes))
                   self.table_widget_production.setColumnCount(6)
                   self.table_widget_production.setHorizontalHeaderLabels(["Image", "Année de registre", "Numéro d'acte", "Nom principal", "Prénom principal", "Code commune"])
        for row, acte in enumerate(actes):
            if self.famille_selected.cdc.nom_cdc == "LOG" and re.search(r'NAISSAN|^RECONNAIS', self.famille_selected.nom_famille):
                infos = [acte.nom_fichier, acte.numero_registre, acte.numero_acte, acte.nom_principal, acte.prenom_principal, acte.code_commune]
                for col, info in enumerate(infos):
                    self.table_widget_production.setItem(row, col, QTableWidgetItem(info))

    """
    etat du progression des actes traités
    """
    def setValueProgressBar(self):
        self.progress_bar.setValue(round(self.getCountRowActe() * 100 / (len(self.list_images))))

    def nextImage(self):
        if self.current_index_image == self.stacked_widget_images.count() - 1:
            QMessageBox.information(None, "Erreur", "Il n'y a plus d'image")
            # self.deleteLater() # detruire la fenetre
            return
        
        self.current_index_image += 1
        self.setCurrentImages()

    def previousImage(self):
        if self.current_index_image == 0:
            QMessageBox.information(None, "Erreur", "Il n'y a plus d'image")
            return
        
        self.current_index_image -= 1
        self.setCurrentImages()
        
    def setCurrentImages(self):
        self.stacked_widget_images.setCurrentIndex(self.current_index_image)
        self.stacked_widget_images.setCurrentWidget(self.stacked_widget_images.widget(self.current_index_image))


    def setCurrentFileNameWidget(self):
        self.table_widget_file_name.changeCurrentItem(self.current_index_image) #mettre en subrillance l'item courant

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
        #image suivant
        if event.key() == Qt.Key_F7:
            self.nextImage()
            self.setCurrentFileNameWidget()
        #image précedent
        elif event.key() == Qt.Key_F3:
            self.previousImage()
            self.setCurrentFileNameWidget()

        #zoom images
        if event.modifiers() & Qt.ControlModifier:
            if event.key() == Qt.Key_Plus or event.key() == Qt.Key_Equal:  # "+" peut être aussi "=" sur certains claviers
                self.zoom()
            elif event.key() == Qt.Key_Minus:
                self.zoom(False)
          
    def zoom(self, is_zoom_plus = True):
            graphic_viewer = self.stacked_widget_images.currentWidget()
            if is_zoom_plus:
                graphic_viewer.scale(MasqueWindow.ZOOM_FACTOR_IN, MasqueWindow.ZOOM_FACTOR_IN)  # Zoom avant
            else:
                graphic_viewer.scale(MasqueWindow.ZOOM_FACTOR_OUT, MasqueWindow.ZOOM_FACTOR_OUT)  # Zoom avant

    def onCellDoubleClickedTableFileName(self, row, column):
        self.current_index_image = row
        self.setCurrentFileNameWidget()
        self.setCurrentImages()
        # self.stacked_widget_images.setCurrentIndex(self.current_index_image)
        # self.stacked_widget_images.setCurrentWidget(self.stacked_widget_images.widget(self.current_index_image))

    def onOpenDialogRoles(self):
        dialog_widget_roles = DialogRoles()
        dialog_widget_roles.exec_()

    def onOpenDialogUser(self):
        dialog_widget_user = DialogUser()
        dialog_widget_user.exec_()
        
    def onOpenDialogChamps(self):
        dialog_widget_champs = DialogCdcFamille()
        dialog_widget_champs.exec_()

    # def onOpenDialogTypeChamps(self):
    #     dialog_widget_type_champs = DialogTypeChamps()
    #     dialog_widget_type_champs.exec_()

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