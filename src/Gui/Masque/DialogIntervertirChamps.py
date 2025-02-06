from PyQt5.QtWidgets import QDialog, QVBoxLayout, QRadioButton, QTableWidgetItem, QMessageBox, QTableWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from PyQt5.uic import loadUi
from src.Model.Cdc import Cdc
from src.Model.Famille import Famille
from src.Model.TypeActe import TypeActe
from src.Model.Champs import Champs

class DialogIntervertirChamps(QDialog):

    def __init__(self):
        super().__init__()

        loadUi('src/Gui/Masque/dialogIntervertirChamps.ui', self)
    
        self.cdc_selected = None
        self.famille_selected = None

        self.registre_selected = None
        self.index_row_selected = None
        self.text_item_selected = None
        self.default_color_champs = self.table_widget_champs.palette().color(QPalette.Base)

        self.initWidget("cdc")

        self.btn_bas.clicked.connect(self.moveChamps)
        self.btn_haut.clicked.connect(self.moveChamps)
        self.btn_save.clicked.connect(self.onSave)

        self.table_widget_cdc.cellClicked.connect(self.onCellTableWidgetCdcClicked)
        self.table_widget_famille.cellClicked.connect(self.onCellTableWidgetFamilleClicked)
        self.table_widget_champs.cellClicked.connect(self.onCellChampsClicked)

        self.resize(1300, 550)

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
            case 'champs':
                data_recorded = Champs.select().where(Champs.famille == self.famille_selected).order_by(Champs.position)
                table_widget_selected = self.table_widget_champs
                table_widget_selected.setColumnCount(1)
                table_widget_selected.setHorizontalHeaderLabels(["Libellé champs"])

        table_widget_selected.setRowCount(len(data_recorded))
        for row,value in enumerate(data_recorded):
            infos = list()
            if type == 'cdc':
                infos.append(value.nom_cdc)
            elif type == 'famille':
                infos.append(value.nom_famille)
            elif type == "champs":
                infos.append(value.label_champ)
            for col, info in enumerate(infos):
                table_widget_selected.setItem(row, col, QTableWidgetItem(info))
                table_widget_selected.setColumnWidth(0, 250)

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
        self.cellSelect('cdc', row)
        self.initWidget("famille")

    def onCellTableWidgetFamilleClicked(self, row):
        self.cellSelect('famille', row)
        self.initWidget('champs')

    def initDefaultBackgroundChamps(self):
        for row in range(self.table_widget_champs.rowCount()):
            self.table_widget_champs.item(row, 0).setBackground(self.default_color_champs)

    def onCellChampsClicked(self, row, column):
        self.initDefaultBackgroundChamps()
        self.index_row_selected = row
        self.text_item_selected = self.table_widget_champs.item(row, column).text()

    def moveChamps(self):
        btn_sender_signal = self.sender()
        name_btn = btn_sender_signal.objectName()
        position_current = self.index_row_selected

        if self.index_row_selected is None:
            self.dialogMessage("erreur", "Erreur", "Veuillez selectionner le champs à déplacer")
            return
        match name_btn:
            case 'btn_haut':
                if self.index_row_selected == 0:
                    self.dialogMessage("erreur", "Erreur", "Impossible de déplacer cette champs vers le haut")
                    return
                self.index_row_selected -= 1
                self.permuteChamps(position_current)
            case 'btn_bas':
                """
                informe l'utilisateur qu'on est à la fin du champs
                """
                if self.index_row_selected == len(Champs.select().where(Champs.famille == self.famille_selected)) - 1:
                    self.dialogMessage("erreur", "Erreur", "Impossible de déplacer cette champs vers le bas")
                    return

                self.index_row_selected += 1
                self.permuteChamps(position_current)
                
                
    def permuteChamps(self, position_current):
        position_permute = self.index_row_selected
        text_item_permute = self.table_widget_champs.item(position_permute, 0).text()

        """on interchange la position dans la vue"""
        self.table_widget_champs.setItem(position_permute,0, QTableWidgetItem(self.text_item_selected))
        self.table_widget_champs.setItem(position_current, 0, QTableWidgetItem(text_item_permute))

        #on definit la couleur du champs qui est actuelement selectionné
        self.table_widget_champs.item(position_permute, 0).setBackground(QColor("lightblue"))

    def onSave(self):
        for i in range(self.table_widget_champs.rowCount()):
            label_champ = self.table_widget_champs.item(i,0).text()
            """
            redefinition du position par ordre d'apparition dans le widget
            e.g: 1er ligne sexe, donc position du sexe => 1
                 2em ligne date, donc position de la date => 2
                 etc
            """
            position = i+1
            q = Champs.update({Champs.position: position}).where((Champs.label_champ == label_champ) & (Champs.famille == self.famille_selected))
            q.execute()
        self.dialogMessage("success", "Success", "Les champs sont organisées avec success")
        
    def dialogMessage(self, type, title, content):
        if type == "erreur":
             QMessageBox.critical(self, title, content)
        elif type == "success":
            QMessageBox.information(self, title, content)



