from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QDoubleSpinBox,
    QPushButton, QScrollArea, QSizePolicy,
    QDialog, QButtonGroup, QRadioButton,
    QMessageBox, QDialogButtonBox
)
from PySide6.QtCore import Qt
from Widgets.Mrua import WidgetMRUA

class PaginaMrua(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        main_layout.addWidget(scroll)

        content = QWidget()
        content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        scroll.setWidget(content)

        layout = QVBoxLayout(content)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(30)

        texto = QLabel()
        texto.setTextFormat(Qt.RichText)
        texto.setWordWrap(True)
        texto.setStyleSheet("font-size:16px;")
        texto.setText("""
        <h2>¿Qué es MRUA?</h2>
        <p>El <b>Movimiento Rectilíneo Uniformemente Acelerado</b> (MRUA) es aquel en el que 
        un objeto se desplaza en línea recta con una aceleración constante.</p>

        <h2>Elementos Clave</h2>
        <ul style="font-size:14pt;">
          <li><b>Posición (s)</b>: distancia recorrida desde el origen.</li>
          <li><b>Velocidad inicial (v₀)</b>: velocidad en el instante t = 0.</li>
          <li><b>Aceleración (a)</b>: tasa de cambio de la velocidad, constante.</li>
          <li><b>Tiempo (t)</b>: intervalo transcurrido desde el inicio del movimiento.</li>
        </ul>

        <h2>Fórmula</h2>
        <p style="text-align:center; font-size:20pt;">
          <b>s = v₀·t + ½·a·t²</b>
        </p>
        <p>La componente <code>v₀·t</code> corresponde al desplazamiento si la velocidad fuera constante, 
        y <code>½·a·t²</code> añade el efecto de la aceleración durante el tiempo <i>t</i>.</p>

        <h2>¿Por qué s = v₀·t + ½·a·t²?</h2>
        <p>Imagina dividir el intervalo de tiempo en pequeños tramos donde la velocidad varía linealmente. 
        El término <code>½·a·t²</code> surge de integrar la aceleración constante para obtener el incremento 
        adicional de distancia sobre el movimiento uniforme.</p>
        """)
        layout.addWidget(texto)

        contenido_layout = QHBoxLayout()
        contenido_layout.setSpacing(40)

        controles = QVBoxLayout()
        controles.setSpacing(15)

        lbl_formula = QLabel("s = v₀·t + ½·a·t²")
        lbl_formula.setStyleSheet("font-size:24px; font-weight:bold;")
        controles.addWidget(lbl_formula)

        self.spin_v0 = QDoubleSpinBox()
        self.spin_v0.setPrefix("v₀ = ")
        self.spin_v0.setRange(0, 20)
        self.spin_v0.setSingleStep(0.1)
        self.spin_v0.setValue(0.0)
        self.spin_v0.setStyleSheet("font-size:16px;")
        controles.addWidget(self.spin_v0)

        self.spin_a = QDoubleSpinBox()
        self.spin_a.setPrefix("a = ")
        self.spin_a.setRange(-10, 10)
        self.spin_a.setSingleStep(0.1)
        self.spin_a.setValue(0.0)
        self.spin_a.setStyleSheet("font-size:16px;")
        controles.addWidget(self.spin_a)

        self.spin_t = QDoubleSpinBox()
        self.spin_t.setPrefix("t = ")
        self.spin_t.setRange(0.1, 20)
        self.spin_t.setSingleStep(0.1)
        self.spin_t.setValue(2.0)
        self.spin_t.setStyleSheet("font-size:16px;")
        controles.addWidget(self.spin_t)

        btn_reset = QPushButton("Restablecer")
        btn_reset.setStyleSheet(
            "background-color:#4285F4; color:white; "
            "border:none; border-radius:4px; font-size:14px; padding:6px;"
        )
        controles.addWidget(btn_reset)
        controles.addStretch()

        contenido_layout.addLayout(controles, 1)

        grafico = QVBoxLayout()
        self.widget_mrua = WidgetMRUA()
        grafico.addWidget(self.widget_mrua)
        grafico.addStretch()
        contenido_layout.addLayout(grafico, 2)

        layout.addLayout(contenido_layout)

        self.lbl_result = QLabel()
        self.lbl_result.setStyleSheet("font-size:18px; font-weight:bold;")
        layout.addWidget(self.lbl_result)

        self.spin_v0.valueChanged.connect(self.actualizar)
        self.spin_a.valueChanged.connect(self.actualizar)
        self.spin_t.valueChanged.connect(self.actualizar)

        btn_reset.clicked.connect(self.reset)
        self.actualizar()
        
        btn_quiz = QPushButton("¡Haz el Quiz!")
        btn_quiz.setStyleSheet("font-size:16px; padding:10px;")
        btn_quiz.clicked.connect(self.mostrar_quiz)
        layout.addWidget(btn_quiz)

    def actualizar(self):
        v0 = self.spin_v0.value()
        a  = self.spin_a.value()
        t  = self.spin_t.value()

        self.widget_mrua.set_parameters(v0, a)
        self.widget_mrua.set_tiempo(t)

        s = v0 * t + 0.5 * a * t * t
        self.lbl_result.setText(f"s = {v0:.2f}·{t:.2f} + ½·{a:.2f}·{t:.2f}² = {s:.2f} m")

    def reset(self):
        self.spin_v0.setValue(0.0)
        self.spin_a.setValue(0.0)
        self.spin_t.setValue(1.0)

    def mostrar_quiz(self):
        preguntas = [
            {
                "pregunta": "¿Cuál es la fórmula para calcular la posición s en MRUA?",
                "opciones": [
                    ("s = v₀·t + ½·a·t²", True),
                    ("s = v₀ + a·t", False),
                    ("s = a·t²", False),
                    ("s = v₀·t - ½·a·t²", False)
                ]
            },
            {
                "pregunta": "En MRUA, ¿qué representa la variable 'a'?",
                "opciones": [
                    ("La aceleración constante", True),
                    ("La velocidad inicial", False),
                    ("El tiempo transcurrido", False),
                    ("La posición inicial", False)
                ]
            },
            {
                "pregunta": "Si la aceleración es negativa en MRUA, ¿qué tipo de movimiento se produce?",
                "opciones": [
                    ("Movimiento desacelerado", True),
                    ("Movimiento acelerado", False),
                    ("Movimiento uniforme", False),
                    ("Movimiento circular", False)
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