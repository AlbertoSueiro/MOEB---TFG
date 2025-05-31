from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtGui import QPainter, QPen, QFont, QBrush, QColor
from PySide6.QtCore import Qt, QPointF
import math

class WidgetAreaCirculo(QWidget):
    MARGEN = 10
    GROSOR_LINEA = 3
    FUENTE = ("Arial", 12)
    COLOR_RELLENO = QColor(240, 200, 100, 150)
    PIXELES_POR_UNIDAD = 10  

    def __init__(self, radio: float = 5.0):
        super().__init__()
        self.radio = radio
        self.setMinimumSize(300, 300)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def establecer_radio(self, r: float):
        self.radio = r
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()  - 2*self.MARGEN
        h = self.height() - 2*self.MARGEN
        cx = self.MARGEN + w/2
        cy = self.MARGEN + h/2

        r_px = self.radio * self.PIXELES_POR_UNIDAD

        painter.setBrush(QBrush(self.COLOR_RELLENO))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPointF(cx, cy), r_px, r_px)

        pen = QPen(Qt.black, self.GROSOR_LINEA)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(QPointF(cx, cy), r_px, r_px)

        painter.setFont(QFont(*self.FUENTE))
        painter.drawLine(cx - r_px, cy, cx + r_px, cy)  

        painter.drawText(cx + r_px + 5, cy,    f"r = {self.radio:.2f}")

        painter.end()