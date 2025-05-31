from PySide6.QtWidgets import  QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QDoubleSpinBox, QSlider
from PySide6.QtCore import Qt
from Widgets.Area_Circulo import WidgetAreaCirculo
import math
import sys

class SimuladorAreaCirculo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20,20,20,20)
        layout.setSpacing(20)

        contenido = QHBoxLayout()
        contenido.setSpacing(40)

        izq = QVBoxLayout()
        izq.setSpacing(10)

        self.spin_r = QDoubleSpinBox()
        self.spin_r.setPrefix("r = ")
        self.spin_r.setRange(1, 10)
        self.spin_r.setSingleStep(0.1)
        self.spin_r.setValue(5)
        izq.addWidget(self.spin_r)

        self.slider_r = QSlider(Qt.Horizontal)
        self.slider_r.setRange(5, 100)
        self.slider_r.setValue(int(self.spin_r.value()*10))
        izq.addWidget(self.slider_r)

        self.lbl_res = QLabel()
        self.lbl_res.setStyleSheet("font-size:16px; font-weight:bold; margin-top:10px;")
        izq.addWidget(self.lbl_res)
        izq.addStretch()

        der = QVBoxLayout()
        self.circulo = WidgetAreaCirculo(radio=self.spin_r.value())
        der.addWidget(self.circulo)
        der.addStretch()

        contenido.addLayout(izq, 1)
        contenido.addLayout(der, 2)
        layout.addLayout(contenido)

        self.slider_r.valueChanged.connect(lambda v: self.spin_r.setValue(v/10))
        self.spin_r.valueChanged.connect(lambda v: self.slider_r.setValue(int(v*10)))
        self.spin_r.valueChanged.connect(self.actualizar)

        self.actualizar(self.spin_r.value())

    def actualizar(self, r):
        self.circulo.establecer_radio(r)
        area = math.pi * r**2
        self.lbl_res.setText(f"Área = π*r² = 3,14 * {r:.2f} = {area:.2f}")
