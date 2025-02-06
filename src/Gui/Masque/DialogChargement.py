from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QFileDialog,QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal
from src.Model.Cdc import Cdc
from src.Model.Famille import Famille
from distutils.dir_util import copy_tree
from src.Validator.Validator import Validator
from src.Gui.MessageBox.MessageBox import MessageBox

class DialogChargement(QDialog):

    handleAnneePathImage = pyqtSignal(object, object, object, object)

    def __init__(self):
        super().__init__()
        loadUi("src/Gui/Masque/dialogChargement.ui", self)

        self.initWidget("cdc")

        self.images_path = "images"
        self.cdc_selected = None
        self.famille_selected = None
        self.total_files = 0

        self.btn_load_image.clicked.connect(self.onLoadImage)
        self.btn_charger.clicked.connect(self.onCharger)
        self.table_widget_cdc.cellClicked.connect(self.onCellTableWidgetCdcClicked)
        self.table_widget_famille.cellClicked.connect(self.onCellTableWidgetFamilleClicked)

        self.resize(750, 350)

    def initWidget(self, type):
        data_recorded = None
        table_widget_selected = None
        match type:
            case 'cdc':
                data_recorded = Cdc.select().order_by(Cdc.id)
                table_widget_selected = self.table_widget_cdc
                table_widget_selected.setColumnCount(1)
                table_widget_selected.setHorizontalHeaderLabels(["Cdc"])
            case 'famille':
                data_recorded = Famille.select().where(Famille.cdc == self.cdc_selected).order_by(Famille.id)
                table_widget_selected = self.table_widget_famille
                table_widget_selected.setColumnCount(1)
                table_widget_selected.setHorizontalHeaderLabels(["Famille"])

        table_widget_selected.setRowCount(len(data_recorded))
        for row,value in enumerate(data_recorded):
            infos = list()
            if type == 'cdc':
                infos.append(value.nom_cdc)
            elif type == 'famille':
                infos.append(value.nom_famille)

            for col, info in enumerate(infos):
                table_widget_selected.setItem(row, col, QTableWidgetItem(info))
                table_widget_selected.setColumnWidth(0, 250)

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

    """
    redefinition des attributs
    """
    def cellSelect(self, type, row):
        match type:
            case 'famille':
              text_selected = self.table_widget_famille.item(row, 0).text()
              self.famille_selected = Famille.select().where(Famille.nom_famille == text_selected).get()
            case 'cdc':
              text_selected = self.table_widget_cdc.item(row, 0).text()
              self.cdc_selected = Cdc.select().where(Cdc.nom_cdc == text_selected).get()

    def onCellTableWidgetCdcClicked(self, row):
        # text_item_select = self.table_widget_cdc.item(row, column).text()
        # self.cdc_selected = Cdc.select().where(Cdc.nom_cdc == text_item_select).get()
        self.cellSelect('cdc', row)
        self.initWidget('famille')

    def onCellTableWidgetFamilleClicked(self, row, column):
        self.cellSelect('famille', row)
        # text_item_select = self.table_widget_famille.item(row, column).text()
        # self.famille_selected = Famille.select().where(Famille.nom_cdc == text_item_select).get()

    def onCharger(self):
        if self.cdc_selected is None or self.images_path == "images" or self.input_annee_registre.text() == "" or self.famille_selected is None:
            # QMessageBox.warning(self, "Attention", "Veuillez renseigner tous les champs")
            MessageBox.show("critical", "Veuillez renseigner tous les champs")
            return
        """
        check numero registre
        """
        validator = Validator.checkNumeroRegistre(self.input_annee_registre.text(), self.cdc_selected.nom_cdc)
        is_valid, message, content, type_message = validator.get('is_valid'), validator.get('message'), validator.get('value'), validator.get('type')
        if not is_valid:
                match type_message:
                    case 'critical':
                        MessageBox.show(type_message, message)
                        return
        
        self.btn_charger.setEnabled(False)
        self.handleAnneePathImage.emit(content.upper(), self.images_path, self.famille_selected, self.is_1_file_many_acte.isChecked())
        self.accept()


    