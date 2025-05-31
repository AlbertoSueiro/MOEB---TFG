from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QDoubleSpinBox,
    QSlider, QScrollArea, QDialog, QButtonGroup, QRadioButton,
    QMessageBox, QDialogButtonBox, QPushButton
)
from PySide6.QtCore import Qt
from Widgets.Area_cuadrado import WidgetAreaCuadrado

class PaginaAreaCuadrado(QWidget):
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
        <h2>¿Qué es el Área?</h2>
        <p>El <b>área</b> mide la superficie ocupada por una figura plana, 
        expresada en unidades cuadradas (m<sup>2</sup>, cm<sup>2</sup>, etc.).</p>

        <h2>Elementos del Cuadrado</h2>
        <ul style="font-size:14pt;">
          <li><b>Lado (l)</b>: longitud de cualquiera de sus cuatro costados, todos iguales.</li>
          <li><b>Unidad</b>: si l está en metros, el área resultará en metros cuadrados (m<sup>2</sup>).</li>
        </ul>

        <h2>Fórmula del Área</h2>
        <p style="text-align:center; font-size:20pt;">
          <b>Área = l &times; l = l<sup>2</sup></b>
        </p>
        <p>Se eleva al cuadrado porque al multiplicar longitud por anchura, 
        y en el cuadrado ambas son l, obtenemos l×l.</p>

        <h2>¿Por qué l²?</h2>
        <p>Imagina dividir el cuadrado en una rejilla de pequeños cuadrados de lado 1. 
        Tendrás l filas y l columnas de esos unitarios, totalizando l×l casillas.</p>
        """)
        layout.addWidget(texto)

        contenido = QHBoxLayout()
        contenido.setSpacing(40)

        izq = QVBoxLayout()
        izq.setSpacing(15)

        lbl_formula = QLabel("Área = l × l")
        lbl_formula.setStyleSheet("font-size:24px; font-weight:bold;")
        izq.addWidget(lbl_formula)

        self.spin_l = QDoubleSpinBox()
        self.spin_l.setPrefix("l = ")
        self.spin_l.setRange(1, 20)
        self.spin_l.setSingleStep(0.1)
        self.spin_l.setValue(5)
        self.spin_l.setStyleSheet("font-size:16px;")
        izq.addWidget(self.spin_l)

        self.slider_l = QSlider(Qt.Horizontal)
        self.slider_l.setRange(10, 200)
        self.slider_l.setValue(int(self.spin_l.value() * 10))
        izq.addWidget(self.slider_l)

        self.lbl_res = QLabel()
        self.lbl_res.setStyleSheet(
            "font-size:18px; font-weight:bold; margin-top:10px;"
        )
        izq.addWidget(self.lbl_res)
        izq.addStretch()

        contenido.addLayout(izq, 1)

        der = QVBoxLayout()
        self.cuadrado = WidgetAreaCuadrado()
        der.addWidget(self.cuadrado)
        der.addStretch()

        contenido.addLayout(der, 2)
        layout.addLayout(contenido)

        self.slider_l.valueChanged.connect(lambda v: self.spin_l.setValue(v / 10))
        self.spin_l.valueChanged.connect(lambda v: self.slider_l.setValue(int(v * 10)))
        self.spin_l.valueChanged.connect(self.actualizar)
        
        self.actualizar(self.spin_l.value())

        btn_quiz = QPushButton("¡Haz el Quiz!")
        btn_quiz.setStyleSheet("font-size:16px; padding:10px;")
        btn_quiz.clicked.connect(self.mostrar_quiz)
        layout.addWidget(btn_quiz)

    def actualizar(self, lado: float):
        self.cuadrado.establecer_lado(lado)
        area = lado * lado
        self.lbl_res.setText(f"Área = {lado:.2f} × {lado:.2f} = {area:.2f}")

    def mostrar_quiz(self):
        preguntas = [
        {
            "pregunta": "¿Cuál es el área de un cuadrado con lado = 4?",
            "opciones": [("16", True), ("8", False), ("12", False), ("20", False)]
        },
        {
            "pregunta": "¿Qué unidad se usa para expresar el área si el lado está en metros?",
            "opciones": [("Metros", False), ("Metros cuadrados (m²)", True), ("Centímetros", False), ("Centímetros cuadrados (cm²)", False)]
        },
        {
            "pregunta": "Si el lado de un cuadrado se duplica, ¿cómo cambia el área?",
            "opciones": [("Se duplica", False), ("Se cuadruplica", True), ("Se mantiene igual", False), ("Se triplica", False)]
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
