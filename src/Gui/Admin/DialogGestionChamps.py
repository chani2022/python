from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QMessageBox
from PyQt5.uic import loadUi
from src.Model.Champs import Champs

class DialogGestionChamps(QDialog):

    def __init__(self, famille):
        super().__init__()

        loadUi('src/Gui/Admin/dialogGestionChamps.ui', self)

        self.famille = famille
        # self.type_acte_selected = None
        self.champs_selected = None

        self.initChamps()

        """
        signal champs
        """
        self.btn_add_champs.clicked.connect(self.onAddOrEditChamps)
        self.btn_delete_champs.clicked.connect(self.onDeleteChamps)
        self.btn_edit_champs.clicked.connect(self.onEditChamps)
        self.table_widget_champs.cellClicked.connect(self.onCellChampsTableWidgetClicked)

        self.resize(1200, 350)

    def initChamps(self):
        # self.group_box_champs.setTitle(f"Liste des champs ({self.type_acte_selected.nom_type_acte})")
        self.input_label.setFocus() #init focus

        champs = Champs.select().where(Champs.famille == self.famille).order_by(Champs.position)
        self.table_widget_champs.setRowCount(champs.count())
        self.table_widget_champs.setColumnCount(5)
        self.table_widget_champs.setHorizontalHeaderLabels(["Label", "Nom Champ", "Position","Obligatoire", "Type d'acte"])
        #on filtre seulement les champs qui appartiennent au registre demandé
        for i,chps in enumerate(champs):
            infos = [chps.label_champ, chps.name_champs, str(chps.position), str(chps.obligatoire), f"{self.famille.nom_famille}"]
            for j, info in enumerate(infos):
                width = 75
                if j==2 or j==2:
                    width = 45
                #ajuster la taille du cellule pour la colonne type de champs
                if j == 4:
                    width = 200
                self.table_widget_champs.setItem(i,j, QTableWidgetItem(info))
                self.table_widget_champs.setColumnWidth(0, width)

    def onAddOrEditChamps(self):
        label = self.input_label.text().capitalize()
        nom = self.input_nom.text()
        position = Champs.select().where(Champs.famille == self.famille).count() + 1
        obligatoire = self.check_box_obligatoire.isChecked()

        #N'autorise pas les doublons
        if Champs.select().where((Champs.label_champ == label) & (Champs.famille == self.famille)).exists():
            QMessageBox.warning(self, "Attention", f"le libellé {label} existe déjà")
            return
        
        if self.btn_add_champs.text() != 'Editer':
            Champs.create(label_champ=label, name_champs=nom, position=position, obligatoire=obligatoire, famille=self.famille)
        else:
            q=Champs.update(label_champ=label, name_champs=nom, obligatoire=obligatoire).where(Champs.id == self.champs_selected.id)
            q.execute()
            QMessageBox.information(self, "Information", "Modification effectué avec succes")
            # self.champs_selected = None

        #reinitialisation des champs
        self.input_label.setText("")
        self.input_nom.setText("")
        self.btn_add_champs.setText("Ajouter")
        
        self.initChamps()

    def onDeleteChamps(self):
        if self.champs_selected is None:
            QMessageBox.warning(self, "Attention", "Aucun champs n'est selectionné")
            return
        reply = QMessageBox.question(self, "Question", f"Voulez vous vraiment supprimer {self.champs_selected.label_champ}?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            Champs.delete_by_id(self.champs_selected)
            self.champs_selected = None
            self.initChamps()

    def onEditChamps(self):
        self.input_label.setText(self.champs_selected.label_champ)
        self.input_nom.setText(self.champs_selected.name_champs)
        self.check_box_obligatoire.setChecked(self.champs_selected.obligatoire)
        self.btn_add_champs.setText("Editer")

    def onCellChampsTableWidgetClicked(self, row):
        text_selected = self.table_widget_champs.item(row, 0).text()
        self.champs_selected = Champs.select().where(Champs.label_champ == text_selected).get()