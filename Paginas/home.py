from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget)
from Paginas.MRUA import PaginaMrua
from Paginas.Area_triangulo import PaginaAreaTriangulo
from Paginas.Suma import PaginaSuma  

class PaginaHome(QWidget):
    def __init__(self, ir_a_modulo_callback, parent=None):
        super().__init__(parent)
        self.ir_a_modulo = ir_a_modulo_callback 

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(30)

        titulo = QLabel("¿Por dónde quieres comenzar?")
        titulo.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(titulo)

        layout.addLayout(self.crear_recomendacion(
            "¿Quieres aprender lo básico?",
            "Empieza con la suma. Es ideal para entender cómo se combinan cantidades.",
            lambda: self.ir_a_modulo("Suma")
        ))

        layout.addLayout(self.crear_recomendacion(
            "¿Quieres aprender matemáticas?",
            "Explora cómo calcular áreas como la de un triángulo. Una base útil para la geometría.",
            lambda: self.ir_a_modulo("Área Triángulo")
        ))

        layout.addLayout(self.crear_recomendacion(
            "¿Quieres aprender física?",
            "Empieza con el MRUA, una base para entender el movimiento.",
            lambda: self.ir_a_modulo("MRUA")
        ))

        layout.addStretch()

    def crear_recomendacion(self, titulo: str, descripcion: str, funcion_click):
        layout = QVBoxLayout()
        label_titulo = QLabel(titulo)
        label_titulo.setStyleSheet("font-size: 16px; font-weight: bold;")
        label_descripcion = QLabel(descripcion)
        label_descripcion.setWordWrap(True)
        btn_ir = QPushButton("Empezar →")
        btn_ir.clicked.connect(funcion_click)
        layout.addWidget(label_titulo)
        layout.addWidget(label_descripcion)
        layout.addWidget(btn_ir)
        layout.setSpacing(5)
        return layout

