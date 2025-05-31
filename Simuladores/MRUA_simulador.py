import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QDoubleSpinBox, QPushButton
)
from Widgets.Mrua import WidgetMRUA


class SimuladorMRUA(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(20)

        etiqueta_formula = QLabel("s = v0·t + 1/2·a·t²", self)
        etiqueta_formula.setStyleSheet("font-size:18px; font-weight:bold;")
        layout_principal.addWidget(etiqueta_formula)

        layout_contenido = QHBoxLayout()
        layout_contenido.setSpacing(40)
        layout_principal.addLayout(layout_contenido)

        col_controles = QVBoxLayout()
        self.formula_dinamica = QLabel("", self)
        self.formula_dinamica.setStyleSheet("font-size:16px;")
        col_controles.addWidget(self.formula_dinamica)

        self.etiqueta_estado = QLabel("", self)
        self.etiqueta_estado.setStyleSheet(
            "font-size:14px; font-style:italic; color:#555;"
        )
        col_controles.addWidget(self.etiqueta_estado)

        self.spin_vel0 = QDoubleSpinBox(self)
        self.spin_vel0.setPrefix("v0 = ")
        self.spin_vel0.setRange(0, 10)
        self.spin_vel0.setSingleStep(0.1)
        self.spin_vel0.setValue(0.0)
        self.spin_vel0.setMinimumHeight(30)
        self.spin_vel0.setStyleSheet("font-size:14px; padding:4px;")
        col_controles.addWidget(self.spin_vel0)

        self.spin_acel = QDoubleSpinBox(self)
        self.spin_acel.setPrefix("a = ")
        self.spin_acel.setRange(-5, 10)
        self.spin_acel.setSingleStep(0.1)
        self.spin_acel.setValue(0.0)
        self.spin_acel.setMinimumHeight(30)
        self.spin_acel.setStyleSheet("font-size:14px; padding:4px;")
        col_controles.addWidget(self.spin_acel)

        self.spin_tiempo = QDoubleSpinBox(self)
        self.spin_tiempo.setPrefix("t = ")
        self.spin_tiempo.setRange(0.1, 10)
        self.spin_tiempo.setSingleStep(0.1)
        self.spin_tiempo.setValue(2.0)
        self.spin_tiempo.setMinimumHeight(30)
        self.spin_tiempo.setStyleSheet("font-size:14px; padding:4px;")
        col_controles.addWidget(self.spin_tiempo)

        btn_restablecer = QPushButton("Restablecer")
        btn_restablecer.clicked.connect(self.reset)
        btn_restablecer.setMinimumHeight(35)
        btn_restablecer.setStyleSheet(
            "background-color:#4285F4; color:white; border:none; border-radius:4px; font-size:14px; padding:6px;"
        )
        col_controles.addWidget(btn_restablecer)
        col_controles.addStretch()

        layout_contenido.addLayout(col_controles, 1)

        col_simulador = QVBoxLayout()
        self.widget_mrua = WidgetMRUA()
        col_simulador.addWidget(self.widget_mrua)
        col_simulador.addStretch()

        layout_contenido.addLayout(col_simulador, 2)

        self.spin_vel0.valueChanged.connect(self.actualizar)
        self.spin_acel.valueChanged.connect(self.actualizar)
        self.spin_tiempo.valueChanged.connect(self.actualizar)

        self.actualizar()

    def actualizar(self):
        v0 = self.spin_vel0.value()
        a  = self.spin_acel.value()
        t  = self.spin_tiempo.value()

        self.widget_mrua.set_parameters(v0, a)
        self.widget_mrua.set_tiempo(t)

        s = v0 * t + 0.5 * a * t * t
        self.formula_dinamica.setText(
            f"s = {v0:.1f}·{t:.2f} + 1/2·{a:.1f}·{t:.2f}² = {s:.2f} m"
        )

        if a > 0:
            estado = "El objeto está acelerando."
        elif a < 0:
            estado = "El objeto está frenando."
        else:
            estado = "Velocidad constante."
        self.etiqueta_estado.setText(estado)

    def reset(self):
        self.spin_vel0.setValue(0.0)
        self.spin_acel.setValue(0.0)
        self.spin_tiempo.setValue(2.0)


