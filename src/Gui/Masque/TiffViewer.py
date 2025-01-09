from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QLabel, QScrollArea
from PIL import Image
import io

class TiffViewer(QScrollArea):
    def __init__(self, tiff_path):
        super().__init__()
        self.load_tiff(tiff_path)

    def load_tiff(self, tiff_path):
        try:
            # Charger le TIFF avec Pillow
            with Image.open(tiff_path) as img:
                # Convertir en bytes
                img_data = io.BytesIO()
                img.save(img_data, format="PNG")
                img_data.seek(0)

                # Charger les bytes dans un QImage
                qimage = QImage.fromData(img_data.read())
                pixmap = QPixmap.fromImage(qimage)

                # Afficher dans QLabel
                label = QLabel(self)
                label.setPixmap(pixmap)

                self.setWidget(label)
                
                # self.setScaledContents(True)
                # self.resize(pixmap.width(), pixmap.height())
        except Exception as e:
            self.setText(f"Erreur : {e}")