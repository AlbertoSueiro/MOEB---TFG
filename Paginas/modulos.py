from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QScrollArea, QStackedWidget,
    QPushButton, QHBoxLayout, QInputDialog
)
from PySide6.QtCore import Qt
from Util.click_modulo import ClickableLabel
from Paginas.Hipotenusa_triangulo import PaginaHipotenusa
from Paginas.MRUA import PaginaMrua
from Paginas.Area_triangulo import PaginaAreaTriangulo
from Paginas.Area_circulo import PaginaAreaCirculo
from Paginas.Area_cuadrado import PaginaAreaCuadrado
from Paginas.Suma import PaginaSuma
from Widgets.Widget_base import WidgetModuloGenerico
from Util.bbdd import conectar,select_modulos_usuario, select_por_nombre
import Util.variables_globales



class PaginaModulos(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        self.nombre_modulos = [
            "Hipotenusa", "MRUA", "Área Triángulo",
            "Área Círculo", "Área Cuadrado", "Suma"
        ]
        self.paginas_dinamicas = []

        self.contenedor = QWidget()
        self.grid = QGridLayout(self.contenedor)
        self.grid.setContentsMargins(20, 20, 20, 20)
        self.grid.setHorizontalSpacing(15)
        self.grid.setVerticalSpacing(15)
        self.grid.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        self.module_labels = []
        for i, nombre in enumerate(self.nombre_modulos):
            lbl = self.crear_label_modulo(nombre, i)
            self.module_labels.append(lbl)

        self.col_count = 1
        self.actualizar_grid_modulos()

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidget(self.contenedor)

        boton_container = QWidget()
        boton_layout = QHBoxLayout(boton_container)
        boton_layout.setContentsMargins(10, 10, 20, 20)
        boton_layout.setAlignment(Qt.AlignRight | Qt.AlignBottom)

        self.btn_crear = QPushButton("＋")
        self.btn_crear.setToolTip("Crear nuevo módulo")
        self.btn_crear.setFixedSize(50, 50)
        self.btn_crear.setStyleSheet("""
            QPushButton {
                background-color: #7a9cf5;
                color: white;
                border-radius: 20px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: #5b7bdd;
            }
        """)
        self.btn_crear.clicked.connect(self.crear_modulo_personalizado)
        boton_layout.addWidget(self.btn_crear)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.scroll)

        self.pagina_hipotenusa = PaginaHipotenusa()
        self.pagina_mrua = PaginaMrua()
        self.pagina_area_triangulo = PaginaAreaTriangulo()
        self.pagina_area_circulo = PaginaAreaCirculo()
        self.pagina_area_cuadrado = PaginaAreaCuadrado()
        self.pagina_suma = PaginaSuma()

        for pg in (
            self.pagina_hipotenusa,
            self.pagina_mrua,
            self.pagina_area_triangulo,
            self.pagina_area_circulo,
            self.pagina_area_cuadrado,
            self.pagina_suma
        ):
            self.stacked_widget.addWidget(pg)

        self.stacked_widget.currentChanged.connect(self.onPaginaCambiada)

        layout_principal.addWidget(self.stacked_widget)
        layout_principal.addWidget(boton_container)
        self.cargar_modulos_personalizados()

    def crear_label_modulo(self, nombre, indice):
        label = ClickableLabel(f"Módulo {nombre}", self.contenedor)
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

    def actualizar_grid_modulos(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
        for i, lbl in enumerate(self.module_labels):
            fila = i // self.col_count
            col  = i % self.col_count
            self.grid.addWidget(lbl, fila, col)

    def modulo_clicado(self, indice):
        import Widgets.Widget_base
        if indice < len(self.nombre_modulos):
            self.stacked_widget.setCurrentIndex(indice + 1)
        else:
            dyn_idx = indice - len(self.nombre_modulos)
            pagina = self.paginas_dinamicas[dyn_idx]
            Util.variables_globales.titulo_modulo = pagina.windowTitle()
            pagina.cargar_modulo()
            self.stacked_widget.setCurrentWidget(pagina)

    def crear_modulo_personalizado(self):
        titulo, ok = QInputDialog.getText(
            self,
            "Nuevo modulo personalizado",
            "Escribe el título del módulo:"
        )
        if not ok or not titulo.strip():
            return
        titulo = titulo.strip()

        nueva_pagina = WidgetModuloGenerico(titulo=titulo)
        self.paginas_dinamicas.append(nueva_pagina)
        self.stacked_widget.addWidget(nueva_pagina)

        nuevo_indice = len(self.module_labels)
        nueva_lbl = self.crear_label_modulo(titulo, nuevo_indice)
        self.module_labels.append(nueva_lbl)
        self.actualizar_grid_modulos()
        self.recalcular_distribucion()

        Util.variables_globales.titulo_modulo=titulo
        self.stacked_widget.setCurrentWidget(nueva_pagina)

    def mostrar_lista_modulos(self):
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
        disponible = (self.scroll.viewport().width() - self.grid.contentsMargins().left() - self.grid.contentsMargins().right()
        )
        nueva_col_count = max(1, disponible // (min_ancho + espaciado))
        if nueva_col_count != self.col_count:
            self.col_count = nueva_col_count
            ancho_widget = (disponible - espaciado * (self.col_count - 1)) // self.col_count
            for lbl in self.module_labels:
                lbl.setFixedSize(ancho_widget, ancho_widget)
            self.actualizar_grid_modulos()

    def onPaginaCambiada(self, indice):
        self.btn_crear.setVisible(indice == 0)

    def cargar_modulos_personalizados(self):
        conexion = conectar()
        datos= select_por_nombre(conexion,Util.variables_globales.usuario_email)
        if datos is not None:
            modulos_personalizados= select_modulos_usuario(conexion, datos[0])

            titulos_existentes = set()

            for i in modulos_personalizados:
                titulo = i[1]
                if titulo not in titulos_existentes:

                    nueva_pagina = WidgetModuloGenerico(titulo=titulo)
                    self.paginas_dinamicas.append(nueva_pagina)
                    self.stacked_widget.addWidget(nueva_pagina)

                    nuevo_indice = len(self.module_labels)
                    nueva_lbl = self.crear_label_modulo(titulo, nuevo_indice)
                    self.module_labels.append(nueva_lbl)
                    self.actualizar_grid_modulos()
                    self.recalcular_distribucion()
                    titulos_existentes.add(titulo)
            
            
