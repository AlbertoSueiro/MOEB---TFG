import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFileDialog, QMessageBox, QInputDialog, QScrollArea,
    QSizePolicy, QDialog, QComboBox
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Slot
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtPdf import QPdfDocument
from Simuladores.MRUA_simulador import SimuladorMRUA
from Simuladores.Hipotenusa_simulador import SimuladorHipotenusa
from Simuladores.Area_triangulo_simulador import SiumladorAreaTriangulo
from Simuladores.Area_cuadrado_simulador import WidgetAreaCuadrado
from Simuladores.Area_circulo_simulador import WidgetAreaCirculo
from Util.bbdd import insertar_modulo, select_modulos_titulo, conectar, select_por_nombre
import Util.variables_globales

IMAGE_SIZE = 200

class TextMediaRow(QWidget):
    def __init__(self, texto: str = ''):
        super().__init__()
        self.setAcceptDrops(True)
        self.setObjectName("Row")
        self.setStyleSheet("""
            QWidget#Row {
                background: #fff;
                border: 1px solid #ddd;
                border-radius: 8px;
            }
            QWidget#Row:hover {
                background: #f7fbff;
            }
            QLabel#Text {
                font-size: 14px;
                color: #333;
            }
        """)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(16)

        self.label = QLabel(texto, self)
        self.label.setObjectName("Text")
        self.label.setWordWrap(True)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(self.label, 3)

        self.media_layout = QHBoxLayout()
        self.media_layout.setSpacing(8)
        layout.addLayout(self.media_layout, 2)

    def resizeEvent(self, event):
        max_w = int(self.width() * 0.6)
        self.label.setMaximumWidth(max_w)
        super().resizeEvent(event)

    def add_image(self, path: str, cargador= None) -> bool:
        pixmap = QPixmap(path)
        if pixmap.isNull():
            return False
        thumb = pixmap.scaled(
            IMAGE_SIZE, IMAGE_SIZE,
            Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        lbl = QLabel(self)
        lbl.setPixmap(thumb)
        lbl.setFixedSize(thumb.size())
        lbl.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.media_layout.addWidget(lbl)

        if cargador is None:
            guardar_en_bbdd(Util.variables_globales.titulo_modulo, "imagen", path)

        return True

class PdfRow(QWidget):
    def __init__(self, path: str, persistir: bool = True):
        super().__init__()
        self.setObjectName("PdfRow")
        self.setStyleSheet("""
            QWidget#PdfRow {
                background: #fff;
                border: 1px solid #ccc;
                border-radius: 8px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(0)

        self.doc = QPdfDocument(self)
        self.viewer = QPdfView(self)
        self.viewer.setDocument(self.doc)
        self.viewer.setPageMode(QPdfView.PageMode.MultiPage)
        self.viewer.setZoomMode(QPdfView.ZoomMode.FitToWidth)
        self.viewer.setMinimumHeight(500)
        self.viewer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.viewer)

        self.error_label = QLabel(self)
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setWordWrap(True)
        self.error_label.hide()
        layout.addWidget(self.error_label)

        total_min_h = (
            self.viewer.minimumHeight()
            + layout.contentsMargins().top()
            + layout.contentsMargins().bottom()
        )
        self.setMinimumHeight(total_min_h)

        self.doc.statusChanged.connect(self._on_status_changed)
        self.doc.load(path)

        if persistir:
            guardar_en_bbdd(Util.variables_globales.titulo_modulo, "pdf", path)


    @Slot(int)
    def _on_status_changed(self, status):
        if status == QPdfDocument.Status.Error:
            err_msg = f"Error cargando PDF (status={status.name})"
            print(err_msg, file=sys.stderr)
            self.error_label.setText(err_msg)
            self.error_label.show()
        else:
            self.error_label.hide()


class WidgetModuloGenerico(QWidget):
    def __init__(self, titulo="Módulo Multimedia", contenido=""):
        super().__init__()
        self.setWindowTitle(titulo)
        self.resize(900, 700)
        self.setStyleSheet("""
            QWidget#Main { background: #eceff1; }
            QLabel#Header { font-size: 16px; color: #555; }
            QPushButton {
                background: #007acc; color: #fff; border: none;
                border-radius: 4px; padding: 8px 16px;
            }
            QPushButton:hover { background: #005f99; }
            QScrollArea { border: none; }
        """)

        main = QVBoxLayout(self)
        self.setObjectName("Main")
        main.setContentsMargins(16, 16, 16, 16)
        main.setSpacing(12)
        
        if contenido:
            hdr = QLabel(contenido, self)
            hdr.setObjectName("Header")
            hdr.setWordWrap(True)
            main.addWidget(hdr)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        main.addWidget(scroll)

        container = QWidget()
        scroll.setWidget(container)

        self.rows_layout = QVBoxLayout(container)
        self.rows_layout.setContentsMargins(0, 0, 0, 0)
        self.rows_layout.setSpacing(12)
        self.rows_layout.setSizeConstraint(QVBoxLayout.SetMinAndMaxSize)

        selector_layout = QHBoxLayout()
        selector_layout.setContentsMargins(0, 8, 0, 8)

        self.combo = QComboBox()
        self.combo.addItems([
            "MRUA",
            "Hipotenusa",
            "Área Triángulo",
            "Área Cuadrado",
            "Área Círculo",
        ])
        selector_layout.addWidget(self.combo)

        btn_cargar = QPushButton("Cargar simulador")
        btn_cargar.clicked.connect(self.cargar_simulador)
        selector_layout.addWidget(btn_cargar)

        main.addLayout(selector_layout)

        self.sim_container = QVBoxLayout()
        self.rows_layout.addLayout(self.sim_container)

        btns = QHBoxLayout()
        main.addLayout(btns)
        for label, slot in [
            ("Insertar texto", self.insertar_texto),
            ("Insertar imagen", lambda: self.insertar_media('img')),
            ("Insertar PDF",   lambda: self.insertar_media('pdf')),
        ]:
            b = QPushButton(label, self)
            b.clicked.connect(slot)
            btns.addWidget(b)

        self.text_rows = []
        self.ya_cargado = False

    def cargar_simulador(self):
        while self.sim_container.count():
            item = self.sim_container.takeAt(0)
            w = item.widget()
            if w:
                w.setParent(None)

        text = self.combo.currentText()
        if text == "MRUA":
            sim = SimuladorMRUA()
        elif text == "Hipotenusa":
            sim = SimuladorHipotenusa()
        elif text == "Área Triángulo":
            sim = SiumladorAreaTriangulo()
        elif text == "Área Cuadrado":
            sim = WidgetAreaCuadrado()
        elif text == "Área Círculo":
            sim = WidgetAreaCirculo()
        else:
            QMessageBox.warning(self, "Error", "Simulador no reconocido")
            return

        sim.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.sim_container.addWidget(sim)

        guardar_en_bbdd(Util.variables_globales.titulo_modulo,  "modulo", text)

    def insertar_texto(self):
        dlg = QInputDialog(self)
        dlg.setWindowTitle("Insertar texto")
        dlg.setLabelText("Escribe el texto:")
        dlg.setOption(QInputDialog.UsePlainTextEditForTextInput, True)
        dlg.resize(500, 300)
        if dlg.exec() == QDialog.Accepted:
            t = dlg.textValue().strip()
            if t:
                row = TextMediaRow(t)
                self.text_rows.append(row)
                self.rows_layout.addWidget(row)
                guardar_en_bbdd(Util.variables_globales.titulo_modulo,  "texto", t)   

    def insertar_media(self, tipo):
        if tipo == 'img':
            if not self.text_rows:
                QMessageBox.warning(self, "Error", "Primero inserta un texto.")
                return
            row = self.text_rows[-1]
            filt = "Imágenes (*.png *.jpg *.jpeg *.bmp *.gif)"
            path, _ = QFileDialog.getOpenFileName(self, "Selecciona imagen", "", filt)
            if path and not row.add_image(path):
                QMessageBox.warning(self, "Error", "No se pudo cargar la imagen.")
        else:
            path, _ = QFileDialog.getOpenFileName(self, "Selecciona PDF", "", "PDF (*.pdf)")
            if not path:
                return
            pdf_row = PdfRow(path)
            self.rows_layout.addWidget(pdf_row)

    def cargar_modulo(self):

        if self.ya_cargado:
            return
        self.ya_cargado = True

        conexion = conectar()
        datos_user = select_por_nombre(conexion, Util.variables_globales.usuario_email)
        datos_modulo = select_modulos_titulo(conexion, datos_user[0], Util.variables_globales.titulo_modulo)
        if datos_modulo:
            for i in datos_modulo:
                match i[3]:
                    case "modulo":
                        self.combo.setCurrentText(i[4])
                        self.cargar_simulador()
                    case "texto":
                        row = TextMediaRow(i[4])
                        self.text_rows.append(row)
                        self.rows_layout.addWidget(row)
                    case "imagen":
                        if self.text_rows:
                            self.text_rows[-1].add_image(i[4], cargador=True)
                        else:
                            print("No hay texto previo para insertar imagen:", i[4])
                    case "pdf":
                        pdf_row = PdfRow(i[4], persistir=False)
                        self.rows_layout.addWidget(pdf_row)

def guardar_en_bbdd(titulo, tipo, contenido):
    conexion = conectar()
    datos_user = select_por_nombre(conexion, Util.variables_globales.usuario_email)
    insertar_modulo(conexion, datos_user[0], titulo, tipo, contenido)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = WidgetModuloGenerico(
        contenido="Añade texto e inserta imágenes o PDFs (estos últimos en bloque completo)."
    )
    w.show()
    sys.exit(app.exec())
