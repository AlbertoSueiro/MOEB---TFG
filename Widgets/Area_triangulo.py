from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtGui import QPainter, QPen, QFont, QPainterPath, QBrush, QColor
from PySide6.QtCore import Qt, QPointF

class WidgetAreaTriangulo(QWidget):
    MARGEN = 10
    GROSOR_LINEA = 3
    FUENTE = ("Arial", 12)
    COLOR_RELLENO = QColor(100, 150, 240, 100)
    PIXELES_POR_UNIDAD = 25

    def __init__(self, lado_a: float = 5.0, lado_b: float = 5.0):
        super().__init__()
        self.lado_a = lado_a
        self.lado_b = lado_b

        self.setMinimumSize(300, 300)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def establecer_lados(self, lado_a: float, lado_b: float):
        self.lado_a = lado_a
        self.lado_b = lado_b
        self.update()  

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        ancho_disp = self.width() - 2 * self.MARGEN
        alto_disp  = self.height() - 2 * self.MARGEN

        escala = self.PIXELES_POR_UNIDAD

        cx = self.MARGEN + ancho_disp / 2
        cy = self.MARGEN + alto_disp  / 2

        half_w = self.lado_a * escala / 2
        half_h = self.lado_b * escala / 2
        A = QPointF(cx - half_w, cy + half_h)
        B = QPointF(cx - half_w, cy - half_h)
        C = QPointF(cx + half_w, cy + half_h)

        path = QPainterPath(A)
        path.lineTo(B)
        path.lineTo(C)
        path.closeSubpath()

        painter.setBrush(QBrush(self.COLOR_RELLENO))
        painter.setPen(Qt.NoPen)
        painter.drawPath(path)

        pen = QPen(Qt.black, self.GROSOR_LINEA)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)
        
        painter.end()
