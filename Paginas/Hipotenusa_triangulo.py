from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QDoubleSpinBox,
    QSlider, QPushButton, QScrollArea, QSizePolicy, QDialog, QButtonGroup, QRadioButton,
    QMessageBox, QDialogButtonBox
)
from PySide6.QtCore import Qt
from Widgets.Hipotenusa import WidgetTrianguloHipotenusa
import math

class PaginaHipotenusa(QWidget):
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
        <h2>Teorema de Pitágoras</h2>
        <p>En un <b>triángulo rectángulo</b>, los <b>catetos</b> (<i>a</i> y <i>b</i>) forman el ángulo de 90°,
        y la <b>hipotenusa</b> (<i>c</i>) es el lado opuesto al ángulo recto.</p>

        <h2>Elementos Clave</h2>
        <ul style="font-size:14pt;">
          <li><b>Catetos (a, b)</b>: lados que encierran el ángulo recto.</li>
          <li><b>Hipotenusa (c)</b>: el lado más largo, enfrente del ángulo recto.</li>
          <li><b>Unidades</b>: todas las longitudes deben usar la misma unidad (m, cm, etc.).</li>
        </ul>

        <h2>Fórmula</h2>
        <p style="text-align:center; font-size:20pt;">
          <b>c = √(a² + b²)</b>
        </p>
        <p>La relación surge porque los cuadrados construidos sobre los catetos tienen
        áreas <i>a</i>² y <i>b</i>², y su suma es igual al área del cuadrado sobre la hipotenusa:</p>
        <blockquote style="margin-left:20px; font-style:italic;">
          Área(cuadrado sobre c) = Área(cuadrado sobre a) + Área(cuadrado sobre b)
        </blockquote>
        <h2>¿Por qué la raíz?</h2>
        <p>Al sumar <i>a</i>² + <i>b</i>² obtenemos un área; la raíz cuadrada de esa área
        devuelve la longitud <i>c</i> en las mismas unidades que <i>a</i> y <i>b</i>.</p>
        """)
        layout.addWidget(texto)

        contenido = QHBoxLayout()
        contenido.setSpacing(40)

        izq = QVBoxLayout()
        izq.setSpacing(15)

        lbl_formula = QLabel("c = √(a² + b²)")
        lbl_formula.setStyleSheet("font-size:24px; font-weight:bold;")
        izq.addWidget(lbl_formula)

        self.spin_a = QDoubleSpinBox()
        self.spin_a.setPrefix("a = ")
        self.spin_a.setRange(1, 10)
        self.spin_a.setSingleStep(0.1)
        self.spin_a.setValue(3)
        self.spin_a.setStyleSheet("font-size:16px;")
        izq.addWidget(self.spin_a)

        self.slider_a = QSlider(Qt.Horizontal)
        self.slider_a.setRange(10, 100)
        self.slider_a.setValue(int(self.spin_a.value() * 10))
        izq.addWidget(self.slider_a)

        self.spin_b = QDoubleSpinBox()
        self.spin_b.setPrefix("b = ")
        self.spin_b.setRange(1, 10)
        self.spin_b.setSingleStep(0.1)
        self.spin_b.setValue(4)
        self.spin_b.setStyleSheet("font-size:16px;")
        izq.addWidget(self.spin_b)

        self.slider_b = QSlider(Qt.Horizontal)
        self.slider_b.setRange(10, 100)
        self.slider_b.setValue(int(self.spin_b.value() * 10))
        izq.addWidget(self.slider_b)

        self.btn_reset = QPushButton("Restablecer valores")
        izq.addWidget(self.btn_reset)

        self.lbl_result = QLabel()
        self.lbl_result.setStyleSheet("font-size:18px; font-weight:bold; margin-top:10px;")
        izq.addWidget(self.lbl_result)

        self.lbl_pasos = QLabel()
        self.lbl_pasos.setWordWrap(True)
        self.lbl_pasos.setStyleSheet("font-size:14px;")
        izq.addWidget(self.lbl_pasos)
        izq.addStretch()

        contenido.addLayout(izq, 1)

        der = QVBoxLayout()
        self.triangulo = WidgetTrianguloHipotenusa()
        der.addWidget(self.triangulo)
        der.addStretch()

        contenido.addLayout(der, 2)
        layout.addLayout(contenido)

        self.slider_a.valueChanged.connect(lambda v: self.spin_a.setValue(v / 10))
        self.spin_a.valueChanged.connect(lambda v: self.slider_a.setValue(int(v * 10)))
        self.slider_b.valueChanged.connect(lambda v: self.spin_b.setValue(v / 10))
        self.spin_b.valueChanged.connect(lambda v: self.slider_b.setValue(int(v * 10)))

        self.spin_a.valueChanged.connect(lambda v: self.actualizar(v, self.spin_b.value()))
        self.spin_b.valueChanged.connect(lambda v: self.actualizar(self.spin_a.value(), v))
        self.btn_reset.clicked.connect(self.reset_valores)

        self.actualizar(self.spin_a.value(), self.spin_b.value())

        btn_quiz = QPushButton("¡Haz el Quiz!")
        btn_quiz.setStyleSheet("font-size:16px; padding:10px;")
        btn_quiz.clicked.connect(self.mostrar_quiz)
        layout.addWidget(btn_quiz)

    def actualizar(self, a: float, b: float):
        self.triangulo.establecer_lados(a, b)
        c = math.hypot(a, b)
        self.lbl_result.setText(f"c = √({a:.2f}² + {b:.2f}²) = {c:.2f}")

        suma = a*a + b*b
        pasos = (
            f"Desarrollo:\n"
            f" a² + b² = {a:.2f}² + {b:.2f}² = {a*a:.2f} + {b*b:.2f} = {suma:.2f}\n"
            f" c = √{suma:.2f} = {c:.2f}"
        )
        self.lbl_pasos.setText(pasos)

    def reset_valores(self):
        self.spin_a.setValue(3)
        self.spin_b.setValue(4)

    def mostrar_quiz(self):
        preguntas = [
          {
              "pregunta": "¿Cuál es la hipotenusa de un triángulo rectángulo con catetos a = 3 y b = 4?",
              "opciones": [("5", True), ("6", False), ("7", False), ("8", False)]
          },
          {
              "pregunta": "¿Qué lados forman el ángulo recto en un triángulo rectángulo?",
              "opciones": [
                  ("Los catetos", True),
                  ("La hipotenusa", False),
                  ("Cualquier par de lados", False),
                  ("Los lados iguales", False)
              ]
          },
          {
              "pregunta": "¿Por qué se usa la raíz cuadrada en la fórmula c = √(a² + b²)?",
              "opciones": [
                  ("Porque la suma a² + b² da un área, y la raíz devuelve la longitud c", True),
                  ("Porque la raíz convierte longitudes en áreas", False),
                  ("Para calcular el perímetro del triángulo", False),
                  ("Para obtener el doble del valor de c", False)
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