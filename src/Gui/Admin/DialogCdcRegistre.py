from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QInputDialog, QMessageBox, QTableWidget
from PyQt5.uic import loadUi
from src.Model.Cdc import Cdc
from src.Model.Registre import Registre
from src.Gui.Admin.DialogChamps import DialogChamps

class DialogCdcRegistre(QDialog):

    def __init__(self):
        super().__init__()

        loadUi("src/Gui/Admin/DialogCdcRegistre.ui", self)

        self.initCdc()
        self.cdc_selected = None
        self.registre_selected = None
        self.dialog_champs = None

        self.btn_add_cdc.clicked.connect(self.onAddCdc)
        self.table_widget_cdc.cellClicked.connect(self.onCellCdcTableWidgetClicked)

        self.btn_add_registre.clicked.connect(self.onAddRegistre)
        self.table_widget_registre.cellDoubleClicked.connect(self.onCellRegistreTableWidgetDoubleClicked)
        self.table_widget_registre.setEditTriggers(QTableWidget.NoEditTriggers)

    def initCdc(self):
        max_row = Cdc.select().count()
        max_column = 1

        self.table_widget_cdc.setRowCount(max_row)
        self.table_widget_cdc.setColumnCount(max_column)
        self.table_widget_cdc.setHorizontalHeaderLabels(["nom cdc"])

        for i,cdc in enumerate(Cdc.select()):
            self.table_widget_cdc.setItem(i,0, QTableWidgetItem(cdc.nom_cdc))
            self.table_widget_cdc.setColumnWidth(0, 125)

    def loadRegistre(self):
        registres = Registre.select().where(Registre.cdc== self.cdc_selected)
        max_row = len(registres)
        max_column = 1
        self.table_widget_registre.setRowCount(max_row)
        self.table_widget_registre.setColumnCount(max_column)
        self.table_widget_registre.setHorizontalHeaderLabels(["Registre"])

        for i, registre in enumerate(registres):
            self.table_widget_registre.setItem(i, 0, QTableWidgetItem(registre.type_registre))
            self.table_widget_registre.setColumnWidth(0, 150)
        pass
    
    def onAddCdc(self):
        self.cdc_selected = None #on reinitialise pour forcer l'utilisateur à rechoisir le cdc courant
        text, ok = QInputDialog.getText(self, "Ajout cdc", "Nom cdc:")
        if ok:
            Cdc.create(nom_cdc=text.upper())
            self.initCdc()

    def onCellCdcTableWidgetClicked(self, row, column):
        text_selected = self.table_widget_cdc.item(row, column).text()
        self.cdc_selected = Cdc.select().where(Cdc.nom_cdc == text_selected).get()
        self.loadRegistre()

    def onAddRegistre(self):
        if self.cdc_selected == None:
            QMessageBox.critical(self, "erreur","Veuillez selectionner un Cdc")
            return
        text, ok = QInputDialog.getText(self, "Ajout registre", "type de registre:")
        if ok:
            Registre.create(type_registre=text.upper(), cdc=self.cdc_selected)
            self.loadRegistre()

    def onCellRegistreTableWidgetDoubleClicked(self, row, column):
        text_selected = self.table_widget_registre.item(row, column).text()
        self.registre_selected = Registre.select().where((Registre.type_registre == text_selected) & (Registre.cdc == self.cdc_selected)).get()
        self.dialog_champs = DialogChamps(self.cdc_selected, self.registre_selected)
        self.dialog_champs.exec_()
        pass
        

        






