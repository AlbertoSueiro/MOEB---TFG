from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QDoubleSpinBox,
    QSlider, QScrollArea, QPushButton, QDialog, QDialogButtonBox, QMessageBox,
    QRadioButton, QButtonGroup
)
from PySide6.QtCore import Qt
from Widgets.Area_Circulo import WidgetAreaCirculo
import math

class PaginaAreaCirculo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        main_layout.addWidget(scroll)

        content = QWidget()
        scroll.setWidget(content)

        layout = QVBoxLayout(content)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(30)

        texto = QLabel()
        texto.setTextFormat(Qt.RichText)
        texto.setWordWrap(True)
        texto.setStyleSheet("font-size:16px;")
        texto.setText("""
        <h2>Definición de Área</h2>
        <p>El <b>área</b> de una figura plana mide el espacio que ocupa en el plano, 
        expresado en unidades cuadradas (por ejemplo, m<sup>2</sup>, cm<sup>2</sup>).</p>

        <h2>Elementos del Círculo</h2>
        <ul style="font-size:14pt;">
          <li><b>π (pi)</b>: constante matemática ≈ 3.1416, relación entre la circunferencia y el diámetro de cualquier círculo.</li>
          <li><b>Radio (r)</b>: distancia desde el centro del círculo hasta cualquier punto de su borde.</li>
        </ul>

        <h2>Fórmula del Área</h2>
        <p style="text-align:center; font-size:20pt;">
          <b>Área = π &times; r<sup>2</sup></b>
        </p>
        <p>El factor <code>r<sup>2</sup></code> aparece porque, al crecer el radio, el área aumenta 
        en proporción al cuadrado de esa distancia. Multiplicar por π ajusta esa “expansión cuadrática” 
        al contorno circular.</p>

        <h2>¿Por qué π·r²?</h2>
        <p>Imagina cortar el círculo en infinitas franjas circulares muy finas y “desplegarlas” 
        en rectángulos de altura ≈ r y ancho ≈ dθ·r. Al integrar todas esas franjas desde 0 hasta r, 
        el área total resulta en π·r².</p>
        """)
        layout.addWidget(texto)

        contenido = QHBoxLayout()
        contenido.setSpacing(40)

        izq = QVBoxLayout()
        izq.setSpacing(15)

        lbl = QLabel("Área = π × r²")
        lbl.setStyleSheet("font-size:24px; font-weight:bold;")
        izq.addWidget(lbl)

        self.spin_r = QDoubleSpinBox()
        self.spin_r.setPrefix("r = ")
        self.spin_r.setRange(1, 10)
        self.spin_r.setSingleStep(0.1)
        self.spin_r.setValue(5)
        self.spin_r.setStyleSheet("font-size:16px;")
        izq.addWidget(self.spin_r)

        self.slider_r = QSlider(Qt.Horizontal)
        self.slider_r.setRange(10, 100)
        self.slider_r.setValue(int(self.spin_r.value() * 10))
        izq.addWidget(self.slider_r)

        self.lbl_res = QLabel()
        self.lbl_res.setStyleSheet(
            "font-size:18px; font-weight:bold; margin-top:10px;"
        )
        izq.addWidget(self.lbl_res)
        izq.addStretch()

        der = QVBoxLayout()
        self.circulo = WidgetAreaCirculo(radio=self.spin_r.value())
        der.addWidget(self.circulo)
        der.addStretch()

        contenido.addLayout(izq, 1)
        contenido.addLayout(der, 2)
        layout.addLayout(contenido)

        self.slider_r.valueChanged.connect(lambda v: self.spin_r.setValue(v / 10))
        self.spin_r.valueChanged.connect(lambda v: self.slider_r.setValue(int(v * 10)))
        self.spin_r.valueChanged.connect(self.actualizar)

        self.actualizar(self.spin_r.value())

        btn_quiz = QPushButton("¡Haz el Quiz!")
        btn_quiz.setStyleSheet("font-size:16px; padding:10px;")
        btn_quiz.clicked.connect(self.mostrar_quiz)
        layout.addWidget(btn_quiz)

    def actualizar(self, r):
        self.circulo.establecer_radio(r)
        area = math.pi * r**2
        self.lbl_res.setText(f"Área = π·r² = π·{r:.2f}² = {area:.2f}")

    def mostrar_quiz(self):
        preguntas = [
            {
                "pregunta": "¿Cuál es el área de un círculo con radio r = 3?",
                "opciones": [("9π", True), ("6π", False), ("3π", False), ("12π", False)]
            },
            {
                "pregunta": "¿Qué representa el valor de π (pi)?",
                "opciones": [
                    ("El área de un círculo unitario", False),
                    ("La relación entre circunferencia y diámetro", True),
                    ("La longitud del radio", False),
                    ("Una constante aleatoria", False)
                ]
            },
            {
                "pregunta": "Si duplicamos el radio de un círculo, el área...",
                "opciones": [
                    ("Se duplica", False),
                    ("Se cuadruplica", True),
                    ("Se mantiene igual", False),
                    ("Se triplica", False)
                ]
            }
        ]

        puntaje = 0
        total = len(preguntas)

        for item in preguntas:
            dialog = QDialog(self)
            dialog.setWindowTitle("Pregunta de Quiz")
            dialog.setMinimumWidth(400)

            layout = QVBoxLayout(dialog)

            pregunta_lbl = QLabel(item["pregunta"])
            pregunta_lbl.setStyleSheet("font-size:16px;")
            layout.addWidget(pregunta_lbl)

            grupo = QButtonGroup(dialog)

            for texto, es_correcta in item["opciones"]:
                btn = QRadioButton(texto)
                btn.setStyleSheet("font-size:14px;")
                layout.addWidget(btn)
                grupo.addButton(btn)
                btn.setProperty("correcta", es_correcta)

            botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            layout.addWidget(botones)

            def evaluar():
                for btn in grupo.buttons():
                    if btn.isChecked():
                        if btn.property("correcta"):
                            nonlocal puntaje
                            puntaje += 1
                        dialog.accept()
                        return
                QMessageBox.warning(self, "Aviso", "Selecciona una opción antes de continuar.")

            botones.accepted.connect(evaluar)
            botones.rejected.connect(dialog.reject)

            resultado = dialog.exec()
            if resultado == 0:  
                return

        QMessageBox.information(
            self,
            "Resultado Final",
            f"Has respondido correctamente {puntaje} de {total} preguntas."
        )