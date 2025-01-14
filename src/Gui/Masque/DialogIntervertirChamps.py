from PyQt5.QtWidgets import QDialog, QVBoxLayout, QRadioButton, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.uic import loadUi
from src.Model.Cdc import Cdc
from src.Model.Registre import Registre
from src.Model.Champs import Champs

class DialogIntervertirChamps(QDialog):

    def __init__(self):
        super().__init__()

        loadUi('src/Gui/Masque/dialogIntervertirChamps.ui', self)
    
        self.list_radio_cdcs = list()
        self.cdc_selected = None

        self.list_radio_registres = list()
        self.registre_selected = None
        self.row_selected = None
        self.text_item_selected = None

        self.loadCdc()

        self.btn_bas.clicked.connect(self.moveChamps)
        self.btn_haut.clicked.connect(self.moveChamps)
        self.btn_save.clicked.connect(self.onSave)
        self.table_widget_champs.cellClicked.connect(self.onCellChampsClicked)

    def loadCdc(self):
        group_layout = QVBoxLayout()
        for i,cdc in enumerate(Cdc.select()):
            radio = QRadioButton(cdc.nom_cdc)
            radio.toggled.connect(self.onToggleCdc)
            group_layout.addWidget(radio)
            self.list_radio_cdcs.append(radio)
        self.group_box_cdc.setLayout(group_layout)


    def onToggleCdc(self):
        text_cdc_selected = None
        for radio in self.list_radio_cdcs:
            if radio.isChecked():
                text_cdc_selected = radio.text()

        self.cdc_selected =  Cdc.select().where(Cdc.nom_cdc == text_cdc_selected).get()

        self.loadRegistre()
        self.initTableChamps()

    def initTableChamps(self):
        self.table_widget_champs.setRowCount(0)
        self.table_widget_champs.setColumnCount(1)
        self.table_widget_champs.setHorizontalHeaderLabels(["Champs"])

    
    def loadRegistre(self):
        """Efface le contenu du QGroupBox."""
        layout = self.group_box_registre.layout()
        if layout is not None:
            while layout.count():  # Supprimer tous les widgets
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()#on detruit les enfants du layout
            self.list_radio_registres = list()
        else:
            layout = QVBoxLayout()
        
        registres = Registre.select().where(Registre.cdc == self.cdc_selected)
        
        for registre in registres:
            radio = QRadioButton(registre.type_registre)
            radio.toggled.connect(self.onToggleRegistre)
            layout.addWidget(radio)
            self.list_radio_registres.append(radio)
        self.group_box_registre.setLayout(layout)
        
        

    def onToggleRegistre(self):
        text_registre_selected = None
        for radio in self.list_radio_registres:
            if radio.isChecked():
                text_registre_selected = radio.text()
        self.registre_selected = Registre.select().where((Registre.cdc == self.cdc_selected) & (Registre.type_registre == text_registre_selected)).get()
        self.loadChamps()
        

    def loadChamps(self):
        champs = Champs.select().where(Champs.registre == self.registre_selected).order_by(Champs.position)
        self.table_widget_champs.setRowCount(len(champs))
        self.table_widget_champs.setColumnCount(1)
        self.table_widget_champs.setHorizontalHeaderLabels(["Champs"])
        
        for i, champ in enumerate(champs):
            infos = [champ.label_champ]
            for j, info in enumerate(infos):
                self.table_widget_champs.setItem(i,j, QTableWidgetItem(info))
                self.table_widget_champs.setColumnWidth(0, 150)

    def moveChamps(self):
        btn_sender_signal = self.sender()
        name_btn = btn_sender_signal.objectName()
        position_current = self.row_selected

        if self.row_selected is None:
            self.dialogMessage("erreur", "Erreur", "Veuillez selectionner le champs à déplacer")
            return
        match name_btn:
            case 'btn_haut':
                if self.row_selected == 0:
                    self.dialogMessage("erreur", "Erreur", "Impossible de déplacer cette champs vers le haut")
                    return
                self.row_selected -= 1
                self.permuteChamps(position_current)
            case 'btn_bas':
                if self.row_selected == len(Champs.select().where(Champs.registre == self.registre_selected)) - 1:
                    self.dialogMessage("erreur", "Erreur", "Impossible de déplacer cette champs vers le bas")
                    return

                self.row_selected += 1
                self.permuteChamps(position_current)
                
                
    def permuteChamps(self, position_current):
        position_permute = self.row_selected
        text_item_permute = self.table_widget_champs.item(position_permute, 0).text()

        """on interchange la position, depand s'il a cliqué sur le btn haut ou bas"""
        self.table_widget_champs.setItem(position_permute,0, QTableWidgetItem(self.text_item_selected))
        self.table_widget_champs.setItem(position_current, 0, QTableWidgetItem(text_item_permute))

        #on definit la couleur du champs qui est actuelement selectionné
        self.table_widget_champs.item(position_permute, 0).setBackground(QColor("lightblue"))

    def onSave(self):
        for i in range(self.table_widget_champs.rowCount()):
            label_champ = self.table_widget_champs.item(i,0).text()
            position = i+1
            q = Champs.update({Champs.position: position}).where((Champs.label_champ == label_champ) & (Champs.registre == self.registre_selected))
            q.execute()
        self.dialogMessage("success", "Success", "Les champs sont organisées avec success")
        
    def onCellChampsClicked(self, row, column):
        self.row_selected = row
        self.text_item_selected = self.table_widget_champs.item(row, column).text()

    def dialogMessage(self, type, title, content):
        if type == "erreur":
             QMessageBox.critical(self, title, content)
        elif type == "success":
            QMessageBox.information(self, title, content)



