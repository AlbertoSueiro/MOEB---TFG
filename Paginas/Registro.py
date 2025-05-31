import sys
import re
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLineEdit, QLabel, QPushButton
)
from Util.bbdd import select_por_nombre, insertar_usuarios, conectar
from Util.hash import hashear_pass
import Util.variables_globales

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
class VentanaRegistro(QMainWindow):
    def __init__(self, parent=None):
        super().__init__() 

        pantalla = QApplication.primaryScreen().geometry()
        ancho = int(pantalla.width() * 0.4)
        alto = int(pantalla.height() * 0.5)
        self.resize(ancho, alto)

        self.setWindowTitle("Pantalla Registro")
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
        
        titulo=QLabel("Crear una cuenta")
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

        self.entrada_password2 = QLineEdit()
        self.entrada_password2.setEchoMode(QLineEdit.EchoMode.Password)
        self.entrada_password2.setPlaceholderText("Repetir Contraseña")
        self.entrada_password2.setStyleSheet(ESTILOS)
        layout.addLayout(crear_layout_campo(self.entrada_password2))

        
        boton = QPushButton("Registrate", self)
        boton.setStyleSheet(ESTILOS)
        boton.clicked.connect(self.comprobar_registro)
        layout.addLayout(crear_layout_campo(boton))

        inicio_sesion = QPushButton("Ya tienes cuenta? Inicia sesion aqui", self)
        inicio_sesion.setStyleSheet("""
            QPushButton {
                background-color: #1e1e1e;
                color: white;
                font-size: 12px;
            }
        """)
        inicio_sesion.clicked.connect(self.ir_inicio_sesion)
        layout.addLayout(crear_layout_campo(inicio_sesion))

        layout.addStretch(1)

    def ir_inicio_sesion(self):
        from Paginas.Login import VentanaLogin
        self.ventana_inicio = VentanaLogin()
        self.ventana_inicio.show()
        self.close()


    def comprobar_registro(self):
        from app import MainWindow
        conexion = conectar()

        algomal= False
        expresion_regular_mail = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if self.entrada_email.text() == "":
            self.entrada_email.setStyleSheet(ESTILOS_ERROR)
            self.entrada_email.setPlaceholderText("El email no puede estar vacio")
            algomal= True
            return
        elif not re.match(expresion_regular_mail, self.entrada_email.text()):
            self.entrada_email.setStyleSheet(ESTILOS_ERROR)
            self.entrada_email.setPlaceholderText("Email no valido")
            algomal= True
            return
        else:
            self.entrada_email.setStyleSheet(ESTILOS)
            self.entrada_email.setPlaceholderText("Email")
            if select_por_nombre(conexion,self.entrada_email.text()) != None:
                print("El usuario ya existe")
                self.entrada_email.setText("El usuario ya existe")
                self.entrada_email.setStyleSheet(ESTILOS_ERROR)
                self.entrada_password1.setText("")
                self.entrada_password2.setText("")
            else:
                if self.entrada_password1.text() == "":
                    self.entrada_password1.setStyleSheet(ESTILOS_ERROR)
                    self.entrada_password1.setPlaceholderText("La contraseña no puede estar vacia")
                    algomal= True
                    return
                elif len(self.entrada_password1.text()) < 6:
                    self.entrada_password1.setStyleSheet(ESTILOS_ERROR)
                    self.entrada_password1.setPlaceholderText("Minimo 6 caracteres")
                    algomal= True
                    return
                else:
                    self.entrada_password1.setStyleSheet(ESTILOS)
                    self.entrada_password1.setPlaceholderText("Contraseña")

                if self.entrada_password1.text()  != self.entrada_password2.text() :
                    self.entrada_password2.setStyleSheet(ESTILOS_ERROR)
                    self.entrada_password2.setPlaceholderText("Las contraseñas no coinciden")
                    algomal= True
                    return
                else:
                    self.entrada_password2.setStyleSheet(ESTILOS)
                    self.entrada_password2.setPlaceholderText("Repetir Contraseña")

                if not algomal:
                    pass_hasheada=hashear_pass(self.entrada_password1.text())
                    insertar_usuarios(conexion,self.entrada_email.text(), pass_hasheada)
                    Util.variables_globales.usuario_email = self.entrada_email.text()
                    self.ventana_inicio = MainWindow()
                    self.ventana_inicio.show()
                    self.close()

        if conexion:
            conexion.close()
        else:
            print("No se pudo conectar a la base de datos.")

