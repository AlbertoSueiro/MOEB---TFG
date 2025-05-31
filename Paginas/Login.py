import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,QHBoxLayout, QLabel, QLineEdit, QPushButton)
from PySide6.QtCore import Qt
from .Registro import VentanaRegistro
from Util.bbdd import select_por_nombre, conectar
import Util.variables_globales
from Util.hash import comprobar_password

ESTILOS = """
    QLineEdit {
        background-color: #333333;
        color: white;
        padding: 10px;
        border-radius: 5px;
        font-size: 16px;
    }
    QLabel{
        font-size:18px;
        font-weight:bold;
        margin-bottom:20px;
    }
    QPushButton {
        background-color: #3FA9E0;
        color: white;
        padding: 10px 20px;
        margin: 10px 0;
        font-size: 16px;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #2596BE;
    }
"""

ESTILOS_ERROR = """

    QLineEdit {
        background-color: #333333;
        color: white;
        padding: 10px;
        border-radius: 5px;
        font-size: 16px;
        border: 2px solid #b55454;
    }
"""

class VentanaLogin(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()

        pantalla = QApplication.primaryScreen().geometry()
        ancho = int(pantalla.width() * 0.4)
        alto = int(pantalla.height() * 0.5)
        self.resize(ancho, alto)

        self.setWindowTitle("Pantalla Login")
        self.setStyleSheet("background-color: #1e1e1e; color: white;")
 
        contenedor = QWidget(self)
        self.setCentralWidget(contenedor)
        layout = QVBoxLayout(contenedor)

        layout.addStretch(1)

        def crear_layout_campo(widget):
            h = QHBoxLayout()
            h.addStretch(1)
            h.addWidget(widget, 8)
            h.addStretch(1)
            return h

        titulo=QLabel("Inicia Sesion")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet(ESTILOS)
        layout.addWidget(titulo)

        self.entrada_email = QLineEdit()
        self.entrada_email.setPlaceholderText("Email")
        self.entrada_email.setStyleSheet(ESTILOS)
        layout.addLayout(crear_layout_campo(self.entrada_email))

        self.entrada_password1 = QLineEdit()
        self.entrada_password1.setEchoMode(QLineEdit.EchoMode.Password)
        self.entrada_password1.setPlaceholderText("Contraseña")
        self.entrada_password1.setStyleSheet(ESTILOS)
        layout.addLayout(crear_layout_campo(self.entrada_password1))

        boton = QPushButton("Accede", self)
        boton.setStyleSheet(ESTILOS)
        boton.clicked.connect(self.comprobar_login)
        layout.addLayout(crear_layout_campo(boton))

        regsitro = QPushButton("Aun no tienes cuenta? Registrate aqui", self)
        regsitro.setStyleSheet("""
            QPushButton {
                background-color: #1e1e1e;
                color: white;
                font-size: 12px;
            }
        """)
        regsitro.clicked.connect(self.ir_registro)
        layout.addLayout(crear_layout_campo(regsitro))

        layout.addStretch(1)

    def ir_registro(self):
        self.ventana_inicio = VentanaRegistro()
        self.ventana_inicio.show()
        self.close()
 
    def comprobar_login(self):
        from app import MainWindow
        algomal= False
        datos = select_por_nombre(conectar(),self.entrada_email.text())
        if datos == None:
            self.entrada_email.setStyleSheet(ESTILOS_ERROR)
            self.entrada_email.setPlaceholderText("Email o contraseña incorrectos")
            self.entrada_email.setText("")
            self.entrada_password1.setText("")
            algomal= True
            return
        elif not comprobar_password(datos[2],self.entrada_password1.text()):
            self.entrada_email.setStyleSheet(ESTILOS_ERROR)
            self.entrada_email.setPlaceholderText("Email o contraseña incorrectos")
            self.entrada_email.setText("")
            self.entrada_password1.setText("")
            algomal= True
            return   
        else:
            self.entrada_email.setStyleSheet(ESTILOS)
            self.entrada_email.setPlaceholderText("Email")
            self.entrada_password1.setStyleSheet(ESTILOS)
            self.entrada_password1.setPlaceholderText("Contraseña")

        if not algomal:
            Util.variables_globales.usuario_email = self.entrada_email.text()
            self.ventana_inicio = MainWindow()
            self.ventana_inicio.show()
            self.close()


