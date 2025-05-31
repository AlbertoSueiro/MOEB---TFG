import sys
import math
from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel,
    QDoubleSpinBox, QSlider, QPushButton, QSizePolicy
)
from PySide6.QtCore import Qt
from Widgets.Hipotenusa import WidgetTrianguloHipotenusa


class SimuladorHipotenusa(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        layout_contenido = QHBoxLayout()
        layout_contenido.setSpacing(40)

        izquierda = QVBoxLayout()
        izquierda.setSpacing(10)

        lbl_formula = QLabel("c = √(a² + b²)")
        lbl_formula.setStyleSheet("font-size:20px; font-weight:bold;")
        izquierda.addWidget(lbl_formula)

        self.spin_a = QDoubleSpinBox()
        self.spin_a.setPrefix("a = ")
        self.spin_a.setRange(1, 10)
        self.spin_a.setSingleStep(0.1)
        self.spin_a.setValue(3)
        izquierda.addWidget(self.spin_a)

        self.slider_a = QSlider(Qt.Horizontal)
        self.slider_a.setRange(10, 100)
        self.slider_a.setValue(int(self.spin_a.value() * 10))
        izquierda.addWidget(self.slider_a)

        self.spin_b = QDoubleSpinBox()
        self.spin_b.setPrefix("b = ")
        self.spin_b.setRange(1, 10)
        self.spin_b.setSingleStep(0.1)
        self.spin_b.setValue(4)
        izquierda.addWidget(self.spin_b)

        self.slider_b = QSlider(Qt.Horizontal)
        self.slider_b.setRange(10, 100)
        self.slider_b.setValue(int(self.spin_b.value() * 10))
        izquierda.addWidget(self.slider_b)

        self.btn_reset = QPushButton("Reset valores")
        izquierda.addWidget(self.btn_reset)

        self.lbl_result = QLabel()
        self.lbl_result.setStyleSheet(
            "font-size:16px; font-weight:bold; margin-top:10px;"
        )
        izquierda.addWidget(self.lbl_result)

        self.lbl_pasos = QLabel()
        self.lbl_pasos.setWordWrap(True)
        izquierda.addWidget(self.lbl_pasos)

        izquierda.addStretch()
        layout_contenido.addLayout(izquierda, 1)

        derecha = QVBoxLayout()
        derecha.setContentsMargins(0, 0, 0, 0)
        self.triangulo = WidgetTrianguloHipotenusa()
        derecha.addWidget(self.triangulo)
        derecha.addStretch()
        layout_contenido.addLayout(derecha, 2)

        main_layout.addLayout(layout_contenido)

        self.slider_a.valueChanged.connect(lambda v: self.spin_a.setValue(v / 10))
        self.spin_a.valueChanged.connect(lambda v: self.slider_a.setValue(int(v * 10)))
        self.slider_b.valueChanged.connect(lambda v: self.spin_b.setValue(v / 10))
        self.spin_b.valueChanged.connect(lambda v: self.slider_b.setValue(int(v * 10)))

        self.spin_a.valueChanged.connect(
            lambda v: self.actualizar(v, self.spin_b.value())
        )
        self.spin_b.valueChanged.connect(
            lambda v: self.actualizar(self.spin_a.value(), v)
        )

        self.btn_reset.clicked.connect(self.reset_valores)

        self.actualizar(self.spin_a.value(), self.spin_b.value())

    def actualizar(self, a: float, b: float):
        self.triangulo.establecer_lados(a, b)
        c = math.hypot(a, b)
        self.lbl_result.setText(f"c² = √({a:.2f}² + {b:.2f}²) = {c:.2f}")

        suma = a * a + b * b
        pasos = (
            f"Desarrollo:\n"
            f" c² = {a:.2f}² + {b:.2f}² = {a*a:.2f} + {b*b:.2f} = {suma:.2f}\n"
            f" c = √{suma:.2f} = {c:.2f}"
        )
        self.lbl_pasos.setText(pasos)

    def reset_valores(self):
        self.spin_a.setValue(3)
        self.spin_b.setValue(4)


