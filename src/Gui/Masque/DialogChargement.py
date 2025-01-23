from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QFileDialog,QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal
from src.Model.Cdc import Cdc
from distutils.dir_util import copy_tree

class DialogChargement(QDialog):

    handleAnneePathImage = pyqtSignal(str, str, object)

    def __init__(self):
        super().__init__()
        loadUi("src/Gui/Masque/dialogChargement.ui", self)

        self.initCdc()

        self.images_path = "images"
        self.cdc_selected = None
        self.total_files = 0

        self.btn_load_image.clicked.connect(self.onLoadImage)
        self.btn_charger.clicked.connect(self.onCharger)
        self.table_widget_cdc.cellClicked.connect(self.onCellClicked)

    def initCdc(self):
        cdcs = Cdc.select()
        self.table_widget_cdc.setRowCount(len(cdcs))
        self.table_widget_cdc.setColumnCount(1)
        self.table_widget_cdc.setHorizontalHeaderLabels(["Cdc"])

        for i, cdc in enumerate(cdcs):
            # nom_cdc = self.table_widget_cdc.item(i, 0).text()
            self.table_widget_cdc.setItem(i,0, QTableWidgetItem(cdc.nom_cdc))
            self.table_widget_cdc.setColumnWidth(0, 150)

    def onLoadImage(self):
        self.images_path = "images"
        # # Ouvrir QFileDialog pour sélectionner un dossier
        path_source_folder = QFileDialog.getExistingDirectory(
            self, 
            "Sélectionner un dossier",  # Titre de la boîte de dialogue
            "",  # Répertoire de démarrage (vide = répertoire courant)
            QFileDialog.ShowDirsOnly  # Option : afficher uniquement les dossiers
        )
        if path_source_folder:  # Si un dossier est sélectionné
            root_dir = path_source_folder.split("/")[-1] #le nom du dossier selectionne
            self.label_path_image.setText(path_source_folder)
            filenames = copy_tree(path_source_folder, self.images_path+"/"+root_dir) # copier le dossier et ses sous dossier
            self.total_files = len(filenames)
            # self.scan(self.images_path+"/"+root_dir)
            self.images_path += "/"+root_dir
        pass
    def onCellClicked(self, row, column):
        text_item_select = self.table_widget_cdc.item(row, column).text()
        self.cdc_selected = Cdc.select().where(Cdc.nom_cdc == text_item_select).get()

    def onCharger(self):
        if self.cdc_selected is None or self.images_path == "images" or self.input_annee_registre.text() == "":
            QMessageBox.warning(self, "Attention", "Veuillez renseigner tous les champs")
            return
        
        self.handleAnneePathImage.emit(self.input_annee_registre.text(), self.images_path, self.cdc_selected)
        self.accept()


    