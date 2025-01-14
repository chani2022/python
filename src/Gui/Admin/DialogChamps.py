from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from src.Model.Champs import Champs
from src.Model.TypeChamps import TypeChamps

class DialogChamps(QDialog):

    def __init__(self, cdc, registre):
        super().__init__()
        loadUi('src/Gui/Admin/dialogChamps.ui', self)

        self.registre = registre
        self.init()
        self.group_box_list.setTitle(f"Liste des champs {registre.type_registre} ({cdc.nom_cdc})")
        #initialisation du combo
        self.combo_type_champs.addItem("-Selectionnez une option ...-")
        for type_champs in TypeChamps.select():
            self.combo_type_champs.addItem(type_champs.type_champs)
        # Désactiver le placeholder pour éviter qu'il soit sélectionné après un choix
        self.combo_type_champs.setItemData(0, True, role=Qt.UserRole)
        self.combo_type_champs.resize(200, 35)

        #signal
        self.btn_add_champs.clicked.connect(self.onAddChamps)
        self.resize(1300, 500)

    def init(self):
        self.input_label.setFocus()#on met le focus sur l'input label

        self.table_widget_champs.setRowCount(Champs.select().where(Champs.registre == self.registre).count())
        self.table_widget_champs.setColumnCount(6)
        self.table_widget_champs.setHorizontalHeaderLabels(["Label", "Nom Champ", "Position","Obligatoire", "Type de champs", "Registre"])
        #on filtre seulement les champs qui appartiennent au registre demandé
        for i,champs in enumerate(Champs.select().where(Champs.registre == self.registre).order_by(Champs.position)):
            infos = [champs.label_champ, champs.name_champs, str(champs.position), str(champs.obligatoire), champs.typeChamps.type_champs, self.registre.type_registre]
            for j, info in enumerate(infos):
                width = 150
                #ajuster la taille du cellule pour la colonne type de champs
                if j == 4:
                    width = 200
                self.table_widget_champs.setItem(i,j, QTableWidgetItem(info))
                self.table_widget_champs.setColumnWidth(0, width)
        

    def onAddChamps(self):

        type_champs = self.combo_type_champs.currentText()
        type_champs = TypeChamps.select().where(TypeChamps.type_champs==type_champs)

        label = self.input_label.text().capitalize()
        nom = self.input_nom.text()
        position = Champs.select().where(Champs.registre == self.registre).count() + 1
        obligatoire = self.check_box_obligatoire.isChecked()
        
        Champs.create(label_champ=label, name_champs=nom, position=position, obligatoire=obligatoire, typeChamps=type_champs, registre=self.registre)

        #on vide les champs
        self.input_label.setText("")
        self.input_nom.setText("")
        
        self.init()



    
