from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtGui import QPainter, QBrush, QColor, QFont
from PySide6.QtCore import Qt

class WidgetSuma(QWidget):
    MAX_CIRCULOS = 100  
    RADIO = 15
    ESPACIADO = 10

    def __init__(self, numero1: float = 0, numero2: float = 0):
        super().__init__()
        self.numero1 = numero1
        self.numero2 = numero2

        self.setMinimumSize(300, 200)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def establecer_valores(self, n1: float, n2: float):
        self.numero1 = n1
        self.numero2 = n2
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        total = int(self.numero1 + self.numero2)
        total = min(total, self.MAX_CIRCULOS)

        ancho_widget = self.width()
        x, y = self.ESPACIADO, self.ESPACIADO
        max_por_fila = max(1, (ancho_widget - self.ESPACIADO) // (2 * self.RADIO + self.ESPACIADO))

        painter.setBrush(QBrush(QColor("#3498db")))  
        for i in range(min(int(self.numero1), self.MAX_CIRCULOS)):
            painter.drawEllipse(x, y, 2 * self.RADIO, 2 * self.RADIO)
            x += 2 * self.RADIO + self.ESPACIADO
            if (i + 1) % max_por_fila == 0:
                x = self.ESPACIADO
                y += 2 * self.RADIO + self.ESPACIADO

        painter.setBrush(QBrush(QColor("#2ecc71"))) 
        for i in range(min(int(self.numero2), self.MAX_CIRCULOS - int(self.numero1))):
            painter.drawEllipse(x, y, 2 * self.RADIO, 2 * self.RADIO)
            x += 2 * self.RADIO + self.ESPACIADO
            if (int(self.numero1) + i + 1) % max_por_fila == 0:
                x = self.ESPACIADO
                y += 2 * self.RADIO + self.ESPACIADO

        painter.setPen(Qt.black)
        painter.setFont(QFont("Arial", 14, QFont.Bold))
        texto = f"{self.numero1:.1f} + {self.numero2:.1f} = {self.numero1 + self.numero2:.1f}"
        painter.drawText(self.rect(), Qt.AlignBottom | Qt.AlignHCenter, texto)
