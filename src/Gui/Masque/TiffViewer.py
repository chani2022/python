from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PIL import Image
import io

class TiffViewer(QGraphicsView):
    def __init__(self, tiff_path):
        super().__init__()
        self.load_tiff(tiff_path)

    def load_tiff(self, tiff_path):

        scene = QGraphicsScene()
        self.setScene(scene)
        pixmap_item = None

        extension = tiff_path.split(".")[-1]
        pixmap = None

        if extension != 'tif':
            pixmap = QPixmap(tiff_path)
            pixmap_item = QGraphicsPixmapItem(pixmap)
            scene.addItem(pixmap_item)
        else:
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
                    
                    pixmap_item = QGraphicsPixmapItem(pixmap)
                    scene.addItem(pixmap_item)
                    
            except Exception as e:
                print(f"Erreur : {e}")
        