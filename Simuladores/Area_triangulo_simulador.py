from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QDoubleSpinBox, QSlider
from PySide6.QtCore import Qt
from Widgets.Area_triangulo import WidgetAreaTriangulo  
import sys

class SiumladorAreaTriangulo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(20)

        layout_contenido = QHBoxLayout()
        layout_contenido.setSpacing(40)

        izquierda = QVBoxLayout()
        izquierda.setSpacing(10)

        etiqueta_formula = QLabel("Área = ½ × a × b")
        etiqueta_formula.setStyleSheet("font-size:20px; font-weight:bold;")
        izquierda.addWidget(etiqueta_formula)

        self.spin_a = QDoubleSpinBox()
        self.spin_a.setPrefix("base = ")
        self.spin_a.setRange(1, 10)
        self.spin_a.setSingleStep(0.1)
        self.spin_a.setValue(3)
        izquierda.addWidget(self.spin_a)

        self.slider_a = QSlider(Qt.Horizontal)
        self.slider_a.setRange(10, 100)
        self.slider_a.setValue(int(self.spin_a.value() * 10))
        izquierda.addWidget(self.slider_a)

        self.spin_b = QDoubleSpinBox()
        self.spin_b.setPrefix("altura = ")
        self.spin_b.setRange(1, 10)
        self.spin_b.setSingleStep(0.1)
        self.spin_b.setValue(4)
        izquierda.addWidget(self.spin_b)

        self.slider_b = QSlider(Qt.Horizontal)
        self.slider_b.setRange(10, 100)
        self.slider_b.setValue(int(self.spin_b.value() * 10))
        izquierda.addWidget(self.slider_b)

        self.etiqueta_resultado = QLabel()
        self.etiqueta_resultado.setStyleSheet(
            "font-size:16px; font-weight:bold; margin-top:10px;"
        )
        izquierda.addWidget(self.etiqueta_resultado)
        izquierda.addStretch()

        derecha = QVBoxLayout()
        self.triangulo = WidgetAreaTriangulo()
        derecha.addWidget(self.triangulo)
        derecha.addStretch()

        layout_contenido.addLayout(izquierda, 1)
        layout_contenido.addLayout(derecha, 2)

        layout_principal.addLayout(layout_contenido)

        self.slider_a.valueChanged.connect(lambda v: self.spin_a.setValue(v / 10))
        self.spin_a.valueChanged.connect(lambda v: self.slider_a.setValue(int(v * 10)))

        self.slider_b.valueChanged.connect(lambda v: self.spin_b.setValue(v / 10))
        self.spin_b.valueChanged.connect(lambda v: self.slider_b.setValue(int(v * 10)))

        self.spin_a.valueChanged.connect(lambda v: self.actualizar(v, self.spin_b.value()))
        self.spin_b.valueChanged.connect(lambda v: self.actualizar(self.spin_a.value(), v))

        self.actualizar(self.spin_a.value(), self.spin_b.value())

    def actualizar(self, a, b):
        self.triangulo.establecer_lados(a, b)
        area = 0.5 * a * b
        self.etiqueta_resultado.setText(f"Área = 1/2* {a:.2f}*  {b:.2f} = {area:.2f}")
