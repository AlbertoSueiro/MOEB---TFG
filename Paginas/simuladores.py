from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QScrollArea, QStackedWidget,
    QPushButton, QHBoxLayout, QApplication
)
from PySide6.QtCore import Qt
from Util.click_modulo import ClickableLabel
from Simuladores.MRUA_simulador import SimuladorMRUA
from Simuladores.Area_circulo_simulador import SimuladorAreaCirculo
from Simuladores.Area_cuadrado_simulador import SimuladorAreaCuadrado
from Simuladores.Area_triangulo_simulador import SiumladorAreaTriangulo
from Simuladores.Hipotenusa_simulador import SimuladorHipotenusa
import sys

class PaginaSimuladores(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        self.nombre_simuladores = [
            "Hipotenusa", "MRUA", "Área Triángulo",
            "Área Círculo", "Área Cuadrado"
        ]
        self.paginas_dinamicas = []

        self.contenedor = QWidget()
        self.grid = QGridLayout(self.contenedor)
        self.grid.setContentsMargins(20, 20, 20, 20)
        self.grid.setHorizontalSpacing(15)
        self.grid.setVerticalSpacing(15)
        self.grid.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        self.module_labels = []
        for i, nombre in enumerate(self.nombre_simuladores):
            lbl = self.crear_label_modulo(nombre, i)
            self.module_labels.append(lbl)

        self.col_count = 1
        self.actualizar_grid_simuladores()

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidget(self.contenedor)

        boton_container = QWidget()
        boton_layout = QHBoxLayout(boton_container)
        boton_layout.setContentsMargins(10, 10, 20, 20)
        boton_layout.setAlignment(Qt.AlignRight | Qt.AlignBottom)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.scroll)

        self.pagina_hipotenusa = SimuladorHipotenusa()
        self.pagina_mrua = SimuladorMRUA()
        self.pagina_area_triangulo = SiumladorAreaTriangulo()
        self.pagina_area_circulo = SimuladorAreaCirculo()
        self.pagina_area_cuadrado = SimuladorAreaCuadrado()

        for pg in (
            self.pagina_hipotenusa,
            self.pagina_mrua,
            self.pagina_area_triangulo,
            self.pagina_area_circulo,
            self.pagina_area_cuadrado
        ):
            self.stacked_widget.addWidget(pg)

        layout_principal.addWidget(self.stacked_widget)
        layout_principal.addWidget(boton_container)

    def crear_label_modulo(self, nombre, indice):
        """Crea una etiqueta clickable para el módulo en posición `indice`."""
        label = ClickableLabel(f"Simulador {nombre}", self.contenedor)
        label.setObjectName("ModuleLabel")
        label.setAlignment(Qt.AlignCenter)
        label.setWordWrap(True)
        label.setStyleSheet("""
            QLabel#ModuleLabel {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
            QLabel#ModuleLabel:hover {
                background-color: #f2f2f2;
            }
        """)
        label.clicked.connect(self.crear_handler_modulo(indice))
        return label

    def crear_handler_modulo(self, indice):
        def handler():
            self.modulo_clicado(indice)
        return handler

    def actualizar_grid_simuladores(self):
        """Vuelve a poblar el grid con todas las etiquetas en module_labels."""
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
        for i, lbl in enumerate(self.module_labels):
            fila = i // self.col_count
            col  = i % self.col_count
            self.grid.addWidget(lbl, fila, col)

    def modulo_clicado(self, indice):
        """Navega a la página fija o dinámica según el índice."""
        if indice < len(self.nombre_simuladores):
            self.stacked_widget.setCurrentIndex(indice + 1)
        else:
            dyn_idx = indice - len(self.nombre_simuladores)
            pagina = self.paginas_dinamicas[dyn_idx]
            self.stacked_widget.setCurrentWidget(pagina)
            
    def mostrar_lista_simuladores(self):
        self.stacked_widget.setCurrentIndex(0)

    def showEvent(self, event):
        super().showEvent(event)
        self.recalcular_distribucion()

    def resizeEvent(self, event):
        self.recalcular_distribucion()
        super().resizeEvent(event)

    def recalcular_distribucion(self):
        min_ancho = 200
        espaciado = self.grid.horizontalSpacing()
        disponible = (
            self.scroll.viewport().width()
            - self.grid.contentsMargins().left()
            - self.grid.contentsMargins().right()
        )
        nueva_col_count = max(1, disponible // (min_ancho + espaciado))
        if nueva_col_count != self.col_count:
            self.col_count = nueva_col_count
            ancho_widget = (
                disponible - espaciado * (self.col_count - 1)
            ) // self.col_count
            for lbl in self.module_labels:
                lbl.setFixedSize(ancho_widget, ancho_widget)
            self.actualizar_grid_simuladores()

