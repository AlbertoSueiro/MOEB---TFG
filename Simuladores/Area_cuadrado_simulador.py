from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QDoubleSpinBox, QSlider
from PySide6.QtCore import Qt
from Widgets.Area_cuadrado import WidgetAreaCuadrado
import sys

class SimuladorAreaCuadrado(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(20)

        layout_contenido = QHBoxLayout()
        layout_contenido.setSpacing(40)

        izquierda = QVBoxLayout()
        izquierda.setSpacing(10)

        etiqueta_formula = QLabel("Área = l × l")
        etiqueta_formula.setStyleSheet("font-size:20px; font-weight:bold;")
        izquierda.addWidget(etiqueta_formula)

        self.spin_l = QDoubleSpinBox()
        self.spin_l.setPrefix("lado = ")
        self.spin_l.setRange(1, 20)
        self.spin_l.setSingleStep(0.1)
        self.spin_l.setValue(5)
        izquierda.addWidget(self.spin_l)

        self.slider_l = QSlider(Qt.Horizontal)
        self.slider_l.setRange(10, 200)
        self.slider_l.setValue(int(self.spin_l.value() * 10))
        izquierda.addWidget(self.slider_l)

        self.etiqueta_resultado = QLabel()
        self.etiqueta_resultado.setStyleSheet("font-size:16px; font-weight:bold; margin-top:10px;")
        izquierda.addWidget(self.etiqueta_resultado)
        izquierda.addStretch()

        derecha = QVBoxLayout()
        self.cuadrado = WidgetAreaCuadrado()
        derecha.addWidget(self.cuadrado)
        derecha.addStretch()

        layout_contenido.addLayout(izquierda, 1)
        layout_contenido.addLayout(derecha, 2)
        layout_principal.addLayout(layout_contenido)

        self.slider_l.valueChanged.connect(lambda v: self.spin_l.setValue(v / 10))
        self.spin_l.valueChanged.connect(lambda v: self.slider_l.setValue(int(v * 10)))
        self.spin_l.valueChanged.connect(self.actualizar)

        self.actualizar(self.spin_l.value())

    def actualizar(self, lado):
        self.cuadrado.establecer_lado(lado)
        area = lado * lado
        self.etiqueta_resultado.setText(f"Área = {lado:.2f} × {lado:.2f} = {area:.2f}")
