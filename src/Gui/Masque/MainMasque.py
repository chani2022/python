import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QProgressBar, QStyleFactory
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
        self.images_path = "images"
        
        screen = QApplication.primaryScreen()
        # print(self.id_user)

        self.list_images = list()

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
        #signal cellule tableau
        self.table_widget_file_name.cellClicked.connect(self.onCellTableWidgetClicked)

        #variable pour contenir les boites de dialogue        
        self.dialog_widget_roles = None
        self.dialog_widget_user = None
        self.dialog_widget_champs = None
        self.dialog_widget_type_champs = None
        self.dialog_widget_intervertir_champs = None
        
        if user.roles.type == "user":
            self.action_gestion_roles.setVisible(False)
            self.action_gestion_utilisateur.setVisible(False)
        #action signal
        self.action_chargement.triggered.connect(self.onOpenFileDialog)
        self.action_gestion_roles.triggered.connect(self.onOpenDialogRoles)
        self.action_gestion_utilisateur.triggered.connect(self.onOpenDialogUser)
        self.action_gestion_champs.triggered.connect(self.onOpenDialogChamps)
        self.action_gestion_type_champs.triggered.connect(self.onOpenDialogTypeChamps)
        self.action_intervertir_les_champs.triggered.connect(self.onOpenDialogIntervertirChamps)

        

        self.showMaximized()

        

    def onOpenFileDialog(self):
        # Ouvrir QFileDialog pour sélectionner un dossier
        path_source_folder = QFileDialog.getExistingDirectory(
            self, 
            "Sélectionner un dossier",  # Titre de la boîte de dialogue
            "",  # Répertoire de démarrage (vide = répertoire courant)
            QFileDialog.ShowDirsOnly  # Option : afficher uniquement les dossiers
        )
        if path_source_folder:  # Si un dossier est sélectionné
            root_dir = path_source_folder.split("/")[-1] #le nom du dossier selectionne
            copy_tree(path_source_folder, self.images_path+"/"+root_dir) # copier le dossier et ses sous dossier
            self.scan(self.images_path+"/"+root_dir)

    def scan(self, path):
        for i, file in enumerate(os.scandir(path)):
            if file.is_file():
                scroll_area = TiffViewer(path+"/"+file.name)
                self.stacked_widget_images.addWidget(scroll_area)
                self.list_images.append(path+"/"+file.name)
            else:
                self.scan(path+"/"+file.name)
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
        self.dialog_widget_roles = DialogRoles()
        self.dialog_widget_roles.exec_()

    def onOpenDialogUser(self):
        self.dialog_widget_user = DialogUser()
        self.dialog_widget_user.exec_()
        pass
        # pass
    def onOpenDialogChamps(self):
        self.dialog_widget_champs = DialogCdcRegistre()
        self.dialog_widget_champs.exec_()

    def onOpenDialogTypeChamps(self):
        self.dialog_widget_type_champs = DialogTypeChamps()
        self.dialog_widget_type_champs.exec_()

    def onOpenDialogIntervertirChamps(self):
        self.dialog_widget_intervertir_champs = DialogIntervertirChamps()
        self.dialog_widget_intervertir_champs.exec_()


        

# if __name__ == "__main__":
    
# app = QApplication(sys.argv)
# window = MasqueWindow()
# window.show()

# sys.exit(app.exec_())