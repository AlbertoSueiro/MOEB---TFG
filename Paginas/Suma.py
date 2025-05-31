from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QDoubleSpinBox, QScrollArea,
    QDialog, QButtonGroup, QRadioButton,QMessageBox, QDialogButtonBox, QPushButton
)
from PySide6.QtCore import Qt
from Widgets.Suma import WidgetSuma

class PaginaSuma(QWidget):
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
        <h2>¿Qué es la Suma?</h2>
        <p>La <b>suma</b> es la operación matemática que une dos cantidades 
        (o más) para formar una sola cantidad total.</p>

        <h2>Elementos</h2>
        <ul style="font-size:14pt;">
          <li><b>Sumando A</b>: el primer número.</li>
          <li><b>Sumando B</b>: el segundo número.</li>
          <li><b>Resultado (C)</b>: la cantidad total al juntar A y B.</li>
        </ul>

        <h2>Fórmula</h2>
        <p style="text-align:center; font-size:20pt;">
          <b>C = A + B</b>
        </p>
        <p>Al sumar A y B, imaginamos tener <i>A</i> objetos y agregar <i>B</i> objetos más; 
        el total es <i>C</i> objetos.</p>
        """)
        layout.addWidget(texto)

        contenido = QHBoxLayout()
        contenido.setSpacing(40)

        izq = QVBoxLayout()
        izq.setSpacing(15)

        lbl_formula = QLabel("C = A + B")
        lbl_formula.setStyleSheet("font-size:24px; font-weight:bold;")
        izq.addWidget(lbl_formula)

        self.spin_a = QDoubleSpinBox()
        self.spin_a.setPrefix("A = ")
        self.spin_a.setRange(0, 15)
        self.spin_a.setSingleStep(1)
        self.spin_a.setValue(5)
        self.spin_a.setStyleSheet("font-size:16px;")
        izq.addWidget(self.spin_a)

        self.spin_b = QDoubleSpinBox()
        self.spin_b.setPrefix("B = ")
        self.spin_b.setRange(0, 15)
        self.spin_b.setSingleStep(1)
        self.spin_b.setValue(3)
        self.spin_b.setStyleSheet("font-size:16px;")
        izq.addWidget(self.spin_b)

        self.lbl_res = QLabel()
        self.lbl_res.setStyleSheet("font-size:18px; font-weight:bold; margin-top:10px;")
        izq.addWidget(self.lbl_res)
        izq.addStretch()

        contenido.addLayout(izq, 1)

        der = QVBoxLayout()
        self.widget_suma = WidgetSuma(self.spin_a.value(), self.spin_b.value())
        der.addWidget(self.widget_suma)
        der.addStretch()

        contenido.addLayout(der, 2)
        layout.addLayout(contenido)

        self.spin_a.valueChanged.connect(self.actualizar)
        self.spin_b.valueChanged.connect(self.actualizar)

        self.actualizar()

        btn_quiz = QPushButton("¡Haz el Quiz!")
        btn_quiz.setStyleSheet("font-size:16px; padding:10px;")
        btn_quiz.clicked.connect(self.mostrar_quiz)
        layout.addWidget(btn_quiz)

    def actualizar(self):
        a = self.spin_a.value()
        b = self.spin_b.value()
        c = a + b
        self.widget_suma.establecer_valores(a, b)
        self.lbl_res.setText(f"C = {a:.0f} + {b:.0f} = {c:.0f}")

    def mostrar_quiz(self):
        preguntas = [
          {
              "pregunta": "¿Cuál es el resultado de sumar 7 + 5?",
              "opciones": [("12", True), ("10", False), ("13", False), ("11", False)]
          },
          {
              "pregunta": "¿Qué representa el resultado de una suma?",
              "opciones": [
                  ("La cantidad total al juntar dos números", True),
                  ("El número más pequeño entre los sumandos", False),
                  ("La diferencia entre dos números", False),
                  ("El producto de dos números", False)
              ]
          },
          {
              "pregunta": "Si sumas 0 a un número, ¿qué sucede?",
              "opciones": [
                  ("El número no cambia", True),
                  ("El número se duplica", False),
                  ("El número disminuye", False),
                  ("El resultado es siempre cero", False)
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