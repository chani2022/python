import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QProgressBar, QTableWidget
from PyQt5.QtGui import QKeyEvent
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
import os
from TiffViewer import TiffViewer
from distutils.dir_util import copy_tree
from TableWidgetFilename import TableWidgetFilename
import math

class MasqueWindow(QMainWindow):
    # def __init__(self, id_user):
    def __init__(self):
        super().__init__()
        # Charger le fichier .ui
        loadUi(os.path.abspath("src/Gui/Masque/MainMasque.ui"), self)
        
        # self.id_user = id_user
        self.images_path = "images"
        # Vous pouvez maintenant connecter des signaux et des slots
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
        self.progress_bar.setTextVisible(True)  # Afficher le texte à l'intérieur de la progress bar
        self.status_bar.addWidget(self.progress_bar)

        self.action_chargement.triggered.connect(self.onOpenFileDialog)
        #on cache par defaut le scroll area image, progressbar
        self.scroll_area_list_images.hide()
        self.progress_bar.hide()

        #tableau widget qui contient la liste des nom d'images à saisir
        self.table_widget_file_name = TableWidgetFilename()
        self.table_widget_file_name.cellClickedSignal.connect(self.onCellTableWidgetClicked)
        self.table_widget_file_name.hide()


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
            # self.countFiles(root_dir)
            self.scan(self.images_path+"/"+root_dir)

    def scan(self, path):
        for i, file in enumerate(os.scandir(path)):
            if file.is_file():
                scroll_area = TiffViewer(path+"/"+file.name)
                self.stacked_widget_images.addWidget(scroll_area)
                self.list_images.append(path+"/"+file.name)
            else:
                self.scan(path+"/"+file.name)
        #après le scan, on met a jour et affiche
        self.table_widget_file_name.appendRow(self.list_images)
        # self.table_widget_file_name.setParent(self)
        #on affiche le progress bar et le scroll area list
        self.progress_bar.show()
        self.scroll_area_list_images.setWidget(self.table_widget_file_name)
        self.scroll_area_list_images.show()

    def keyPressEvent(self, event: QKeyEvent):
        """Méthode appelée lorsqu'une touche est pressée."""
        key = event.text()
        modifiers = event.modifiers()
        #image suivant
        if event.key() == Qt.Key_F7:
            if self.stacked_widget_images.currentIndex() == self.stacked_widget_images.count() - 1:
                QMessageBox.information(None, "Erreur", "Il n'y a plus d'images suivant")
                return
            self.imageManipilator()
            self.table_widget_file_name.changeCurrentItem(self.stacked_widget_images.currentIndex())
        #image précedent
        elif event.key() == Qt.Key_F3:
            if self.stacked_widget_images.currentIndex() == 0:
                QMessageBox.information(None, "Erreur", "Il n'y a plus d'images précédent")
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
                width_pixmap += 10
                height_pixmap += 10
            else:
                width_pixmap -= 10
                height_pixmap -= 10

            image_scaled = pixmap.scaled(
                    width_pixmap, height_pixmap, 
                    Qt.KeepAspectRatio,  # Conserver le ratio de l'image
                    Qt.SmoothTransformation  # Transformation lisse pour une meilleure qualité
                    # Qt.FastTransformation
                )
            label.setPixmap(image_scaled)
            scroll_area.setWidget(label)
            self.stacked_widget_images.setCurrentWidget(scroll_area)

    def onCellTableWidgetClicked(self, row, column):
        self.stacked_widget_images.setCurrentIndex(row)
        self.stacked_widget_images.setCurrentWidget(self.stacked_widget_images.widget(row))

            


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MasqueWindow()
    window.show()
    sys.exit(app.exec_())