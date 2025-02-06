from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QInputDialog, QMessageBox, QTableWidget
from PyQt5.uic import loadUi
from src.Model.Cdc import Cdc
from src.Model.Famille import Famille
from src.Model.TypeActe import TypeActe
from src.Gui.Admin.DialogGestionTypeActe import DialogGestionTypeActe
from src.Gui.Admin.DialogGestionChamps import DialogGestionChamps

class DialogCdcFamille(QDialog):

    def __init__(self):
        super().__init__()

        loadUi("src/Gui/Admin/DialogCdcFamille.ui", self)

        self.initCdc()
        self.cdc_selected = None
        self.Famille_selected = None

        self.btn_add_cdc.clicked.connect(self.onAddCdc)
        self.btn_delete_cdc.clicked.connect(self.onDeleteCdc)
        self.table_widget_cdc.cellClicked.connect(self.onCellCdcTableWidgetClicked)
        self.table_widget_cdc.setEditTriggers(QTableWidget.NoEditTriggers) #rendre ineditable

        self.btn_add_famille.clicked.connect(self.onAddFamille)
        self.btn_delete_famille.clicked.connect(self.onDeleteFamille)
        

        self.table_widget_famille.cellClicked.connect(self.onCellFamilleTableWidgetClicked)
        # self.table_widget_famille.cellDoubleClicked.connect(self.onCellFamilleTableWidgetDoubleClicked)
        self.table_widget_famille.setEditTriggers(QTableWidget.NoEditTriggers) #rendre ineditable

        self.btn_gestion_champs.clicked.connect(self.onGestionChamps)
        self.btn_gestion_type_acte.clicked.connect(self.onGestionTypeActe)

    def initCdc(self):
        max_row = Cdc.select().count()
        max_column = 1

        self.table_widget_cdc.setRowCount(max_row)
        self.table_widget_cdc.setColumnCount(max_column)
        self.table_widget_cdc.setHorizontalHeaderLabels(["Cdc"])

        for i,cdc in enumerate(Cdc.select()):
            self.table_widget_cdc.setItem(i,0, QTableWidgetItem(cdc.nom_cdc))
            self.table_widget_cdc.setColumnWidth(0, 125)

    def loadFamille(self):
        Familles = Famille.select().where(Famille.cdc== self.cdc_selected)
        max_row = len(Familles)
        max_column = 1
        self.table_widget_famille.setRowCount(max_row)
        self.table_widget_famille.setColumnCount(max_column)
        self.table_widget_famille.setHorizontalHeaderLabels(["Famille"])

        for i, famille in enumerate(Familles):
            self.table_widget_famille.setItem(i, 0, QTableWidgetItem(famille.nom_famille))
            self.table_widget_famille.setColumnWidth(0, 250)
            
        pass
    
    def onAddCdc(self):
        self.cdc_selected = None
        cdc, ok = QInputDialog.getText(self, "Ajout cdc", "Nom cdc:")
        cdc = cdc.upper()
        if ok:
            if Cdc.select().where(Cdc.nom_cdc == cdc).exists():
                QMessageBox.information(self, "Information", f"le cdc {cdc} existe déjà")
                return
            Cdc.create(nom_cdc=cdc)
            self.initCdc()

    def onDeleteCdc(self):
        if self.cdc_selected is None:
            QMessageBox.information(self, "Information", "Veuillez selectionner le cdc à supprimer!")
            return
        reply = QMessageBox.question(self, "Question", f"Voulez vous vraiment supprimer le cdc {self.cdc_selected.nom_cdc} ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            Cdc.delete_by_id(self.cdc_selected)
            self.cdc_selected = None #indique à l'utilisateur de selectioner a nouveau un cdc à supprimer
            self.initCdc()

    def onCellCdcTableWidgetClicked(self, row, column):
        text_selected = self.table_widget_cdc.item(row, column).text()
        self.cdc_selected = Cdc.select().where(Cdc.nom_cdc == text_selected).get()
        self.loadFamille()

    def onAddFamille(self):
        if self.cdc_selected == None:
            QMessageBox.critical(self, "erreur","Veuillez selectionner un Cdc.")
            return
        famille, ok = QInputDialog.getText(self, "Ajout Famille", "type de Famille:")
        famille = famille.upper()
        if ok:
            if Famille.select().where(Famille.nom_famille == famille).exists():
                QMessageBox.information(self, "Information", f"La famille {famille} du cdc {self.cdc_selected.nom_cdc} existe déjà.")
                return
            
            Famille.create(nom_famille=famille, cdc=self.cdc_selected)
            self.loadFamille()

    def onDeleteFamille(self):
        if self.Famille_selected == None:
            QMessageBox.information(self, "erreur","Veuillez selectionner une famille.")
            return
        reply = QMessageBox.question(self, "Question", f"Voulez vous vraiment supprimer la famille {self.Famille_selected.nom_famille} ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            Famille.delete_by_id(self.Famille_selected)
            self.Famille_selected = None #indique l'utilisateur à selectioner a nouveau un cdc à supprimer
            self.loadFamille()

    def onCellFamilleTableWidgetClicked(self, row, column):
        text_selected = self.table_widget_famille.item(row, column).text()
        self.Famille_selected = Famille.select().where(Famille.nom_famille == text_selected).get()
        

    def onGestionChamps(self):
        if self.cdc_selected is None or self.Famille_selected is None:
            QMessageBox.warning(self, "Attention", "Veuillez selectioner le cdc et la famille")
            return
        dialog_gestion_champs = DialogGestionChamps(self.Famille_selected)
        dialog_gestion_champs.exec_()

    def onGestionTypeActe(self):
        if self.cdc_selected is None or self.Famille_selected is None:
            QMessageBox.warning(self, "Attention", "Veuillez selectioner le cdc et la famille")
            return
        dialog_gestion_type_acte = DialogGestionTypeActe(self.Famille_selected)
        dialog_gestion_type_acte.exec_()

        

        






