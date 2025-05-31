from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt

class WidgetAreaCuadrado(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lado = 5  
        self.setMinimumSize(200, 200)  

    def establecer_lado(self, l):
        self.lado = l
        self.update()  

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.width() < 50 or self.height() < 50:
            return  

        margen = 20
        disponible = min(self.width(), self.height()) - 2 * margen

        escala = disponible / 20
        lado_px = self.lado * escala

        x = (self.width() - lado_px) / 2
        y = (self.height() - lado_px) / 2

        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(QColor("#aaddff"))
        painter.drawRect(x, y, lado_px, lado_px)
