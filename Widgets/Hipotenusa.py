from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtGui import QPainter, QPen, QFont, QPainterPath
from PySide6.QtCore import Qt, QPointF
import math

class WidgetTrianguloHipotenusa(QWidget):
    MARGEN = 20
    GROSOR_LINEA = 3
    GRID_STEP = 25

    def __init__(self, lado_a: float = 3.0, lado_b: float = 4.0):
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
        hip = math.hypot(self.lado_a, self.lado_b)
        escala = (min(ancho_disp, alto_disp) / hip) if hip > 0 else 1.0

        cx = self.MARGEN + ancho_disp / 2
        cy = self.MARGEN + alto_disp  / 2
        half_w = self.lado_a * escala / 2
        half_h = self.lado_b * escala / 2
        A = QPointF(cx - half_w, cy + half_h)
        B = QPointF(cx - half_w, cy - half_h)
        C = QPointF(cx + half_w, cy + half_h)

        pen = QPen(Qt.black, self.GROSOR_LINEA)
        painter.setPen(pen)
        path = QPainterPath(A)
        path.lineTo(B)
        path.lineTo(C)
        path.closeSubpath()
        painter.drawPath(path)

        size = 20
        painter.drawLine(A, QPointF(A.x() + size, A.y()))
        painter.drawLine(A, QPointF(A.x(), A.y() - size))

        painter.setFont(QFont("Arial", 10))
        mid_AB = (A + B) / 2
        painter.drawText(mid_AB.x() - 30, mid_AB.y(), f"b = {self.lado_b:.2f}")
        mid_AC = (A + C) / 2
        painter.drawText(mid_AC.x(), mid_AC.y() + 20, f"a = {self.lado_a:.2f}")
        mid_BC = (B + C) / 2
        painter.drawText(mid_BC.x() + 10, mid_BC.y() - 10, f"c = {hip:.2f}")

        painter.end()
