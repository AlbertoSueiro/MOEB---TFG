from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QDoubleSpinBox,
    QSlider, QScrollArea, QDialog, QButtonGroup, QRadioButton,
    QMessageBox, QDialogButtonBox, QPushButton
)
from PySide6.QtCore import Qt
from Widgets.Area_triangulo import WidgetAreaTriangulo

class PaginaAreaTriangulo(QWidget):
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
        <h2>¿Qué es el Área de un Triángulo?</h2>
        <p>El <b>área</b> de un triángulo mide la superficie encerrada entre sus tres lados, 
        expresada en unidades cuadradas (m<sup>2</sup>, cm<sup>2</sup>, etc.).</p>

        <h2>Elementos Clave</h2>
        <ul style="font-size:14pt;">
          <li><b>Base (b)</b>: uno de los lados del triángulo sobre el que se “apoya”.</li>
          <li><b>Altura (a)</b>: la distancia perpendicular desde el vértice opuesto hasta la base.</li>
          <li><b>Unidades</b>: si las longitudes están en metros, el área resultará en m<sup>2</sup>.</li>
        </ul>

        <h2>Fórmula del Área</h2>
        <p style="text-align:center; font-size:20pt;">
          <b>Área = ½ &times; base &times; altura</b>
        </p>
        <p>Multiplicamos base por altura para obtener el área de un rectángulo de esas dimensiones, 
        y luego dividimos entre dos porque un triángulo es justo la mitad de ese rectángulo.</p>

        <h2>¿Por qué ½·a·b?</h2>
        <p>Si imaginamos dos triángulos idénticos con la misma base y altura y los juntamos por sus bases,
        forman un rectángulo. Así, el área total sería a·b, y cada triángulo cubre la mitad, es decir ½·a·b.</p>
        """)
        layout.addWidget(texto)

        contenido = QHBoxLayout()
        contenido.setSpacing(40)

        izq = QVBoxLayout()
        izq.setSpacing(15)

        lbl_formula = QLabel("Área = ½ × a × b")
        lbl_formula.setStyleSheet("font-size:24px; font-weight:bold;")
        izq.addWidget(lbl_formula)

        self.spin_a = QDoubleSpinBox()
        self.spin_a.setPrefix("b = ")
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
        self.spin_b.setPrefix("a = ")
        self.spin_b.setRange(1, 10)
        self.spin_b.setSingleStep(0.1)
        self.spin_b.setValue(4)
        self.spin_b.setStyleSheet("font-size:16px;")
        izq.addWidget(self.spin_b)

        self.slider_b = QSlider(Qt.Horizontal)
        self.slider_b.setRange(10, 100)
        self.slider_b.setValue(int(self.spin_b.value() * 10))
        izq.addWidget(self.slider_b)

        self.lbl_res = QLabel()
        self.lbl_res.setStyleSheet("font-size:18px; font-weight:bold; margin-top:10px;")
        izq.addWidget(self.lbl_res)
        izq.addStretch()

        contenido.addLayout(izq, 1)

        der = QVBoxLayout()
        self.triangulo = WidgetAreaTriangulo()
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

        self.actualizar(self.spin_a.value(), self.spin_b.value())

        btn_quiz = QPushButton("¡Haz el Quiz!")
        btn_quiz.setStyleSheet("font-size:16px; padding:10px;")
        btn_quiz.clicked.connect(self.mostrar_quiz)
        layout.addWidget(btn_quiz)

    def actualizar(self, a: float, b: float):
        self.triangulo.establecer_lados(a, b)
        area = 0.5 * a * b
        self.lbl_res.setText(f"Área = ½·{a:.2f}·{b:.2f} = {area:.2f}")

    def mostrar_quiz(self):
        preguntas = [
          {
              "pregunta": "¿Cuál es el área de un triángulo con base = 6 y altura = 4?",
              "opciones": [("12", True), ("24", False), ("10", False), ("20", False)]
          },
          {
              "pregunta": "¿Qué representa la altura en un triángulo?",
              "opciones": [
                  ("La distancia perpendicular desde un vértice a la base", True),
                  ("La longitud de la base", False),
                  ("La suma de los lados", False),
                  ("La diagonal del triángulo", False)
              ]
          },
          {
              "pregunta": "¿Por qué se multiplica base por altura y se divide entre 2 para calcular el área?",
              "opciones": [
                  ("Porque el triángulo es la mitad de un rectángulo con esa base y altura", True),
                  ("Porque el triángulo es dos veces un rectángulo", False),
                  ("Para calcular el perímetro", False),
                  ("Porque el área es igual a base más altura", False)
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