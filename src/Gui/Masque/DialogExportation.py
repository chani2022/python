from PyQt5.QtWidgets import QWidget, QDialog, QTableWidgetItem
from PyQt5.uic import loadUi
from src.Model.Cdc import Cdc
from src.Model.Registre import Registre
from src.Model.Production import Production
from src.Model.Champs import Champs
from src.Repository.ProductionRepository import ProductionRepository
from peewee import JOIN
from src.Excel.Excel import Excel

class DialogExportation(QDialog):

    def __init__(self):
        super().__init__()

        loadUi('src/Gui/Masque/dialogExportation.ui', self)

        self.initCdc()

        self.cdc_selected = None
        self.registre_selected = None

        self.headers = ["Nom image", "Année"]
        self.data = dict()
        self.data_to_excel = list()
        self.annee_registre = None

        self.table_widget_cdc.cellClicked.connect(self.onCellClickedCdc)
        self.table_widget_registre.cellClicked.connect(self.onCellClickedRegistre)
        self.btn_exporter.clicked.connect(self.onUpdateTableWidgetAndCreateExcel)

    def initCdc(self):
        cdcs = Cdc.select()
        self.table_widget_cdc.setRowCount(len(cdcs))
        self.table_widget_cdc.setColumnCount(1)
        self.table_widget_cdc.setHorizontalHeaderLabels(["Cdc"])

        for i, cdc in enumerate(cdcs):
            # nom_cdc = self.table_widget_cdc.item(i, 0).text()
            self.table_widget_cdc.setItem(i,0, QTableWidgetItem(cdc.nom_cdc))
            self.table_widget_cdc.setColumnWidth(0, 150)

    def initRegistre(self):
        registres = (Registre
                        .select()
                        .where(Registre.cdc == self.cdc_selected))
        
        self.table_widget_registre.setRowCount(len(registres))
        self.table_widget_registre.setColumnCount(1)
        self.table_widget_registre.setHorizontalHeaderLabels(["Registre"])

        for i, registre in enumerate(registres):
            # nom_cdc = self.table_widget_cdc.item(i, 0).text()
            self.table_widget_registre.setItem(i,0, QTableWidgetItem(registre.type_registre))
            self.table_widget_registre.setColumnWidth(0, 150)


    def onCellClickedCdc(self, row, column):
        text_item_select = self.table_widget_cdc.item(row, column).text()
        self.cdc_selected = Cdc.select().where(Cdc.nom_cdc == text_item_select).get()

        self.initRegistre()

    def onCellClickedRegistre(self, row, column):
        text_item_select = self.table_widget_registre.item(row, column).text()
        self.registre_selected = Registre.select().where(Registre.type_registre == text_item_select).get()

    def onUpdateTableWidgetAndCreateExcel(self):
        self.btn_exporter.setEnabled(False)

        self.annee_registre = self.input_annee.text()
        production_repository = ProductionRepository()
        productions = production_repository.findAllGroupBy(self.cdc_selected, self.registre_selected, self.annee_registre)

        self.updateTableWidgetProduction(productions)
        self.exportToExcel()

    def updateTableWidgetProduction(self, productions):

        for production in productions:
            label = None
            valeur = production.valeur_champ
            nom_image = production.nom_image
            annee_registre = production.annee_registre
            numero_acte = production.numero_acte

            if production.champs is None:
                label = "Type registre"
            else:
                label = production.champs.label_champ

            if label not in self.headers:
                self.headers.append(label)

            if numero_acte not in self.data:
                self.data[numero_acte] = [nom_image, annee_registre, valeur]
            else:
                self.data[numero_acte].append(valeur)

        self.table_widget_production.setColumnCount(len(self.headers))
        self.table_widget_production.setRowCount(len(self.data))
        self.table_widget_production.setHorizontalHeaderLabels(self.headers)
        print(self.data)
        for numero_acte, infos in self.data.items():
            self.data_to_excel.append(infos)
            for row in range(len(infos)):
                for col in range(len(self.headers)):
                    self.table_widget_production.setItem(row, col, QTableWidgetItem(str(infos[col])))

    def exportToExcel(self):
        excel = Excel(self.headers, self.data_to_excel)
        print(self.headers)
        print(f"data {self.data_to_excel}")
        excel.appendData(self.data_to_excel)
        self.progressBar.setValue(round(excel.number_line_appended * 100 / len(self.data_to_excel)))
        excel.save(f"{self.registre_selected.type_registre} ({self.cdc_selected.nom_cdc})-{self.annee_registre}.xlsx")
        pass
        
    