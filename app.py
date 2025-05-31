import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget)
from Paginas.home import PaginaHome
from Paginas.perfil import PaginaPerfil
from Paginas.modulos import PaginaModulos
from Paginas.Asistente import ChatWindow
from Paginas.simuladores import PaginaSimuladores

ESTILOS = """
QMainWindow {
    background-color: #f5f5f5;
}
QWidget#LoginWindow {
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 8px;
}
QLineEdit, QDoubleSpinBox {
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 14px;
}
QLineEdit:focus, QDoubleSpinBox:focus {
    border-color: #7a9cf5;
}
QPushButton {
    background-color: #7a9cf5;
    color: #fff;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-size: 14px;
}
QPushButton:hover {
    background-color: #5b7bdd;
}
QWidget#NavBar {
    background-color: #7a9cf5;
}
QPushButton#NavButton {
    background-color: transparent;
    color: #fff;
    border: none;
    padding: 10px 20px;
    font-size: 15px;
}
QPushButton#NavButton:hover {
    background-color: #5b7bdd;
}
QLabel#ModuleLabel {
    background-color: #fff;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 20px;
    font-size: 16px;
    min-height: 100px;
}
"""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Inicio")
        self.resize(900, 600)
        self.setStyleSheet(ESTILOS)
        
        root = QWidget()
        root_l = QVBoxLayout(root)
        root_l.setContentsMargins(0, 0, 0, 0)
        root_l.setSpacing(0)

        nav = QWidget()
        nav.setObjectName("NavBar")
        h = QHBoxLayout(nav)
        h.setContentsMargins(10, 5, 10, 5)
        h.setSpacing(0)

        self.btn_home = QPushButton("Inicio")
        self.btn_home.setObjectName("NavButton")
        self.btn_modules = QPushButton("Módulos")
        self.btn_modules.setObjectName("NavButton")
        self.btn_simuladores = QPushButton("Simuladores")
        self.btn_simuladores.setObjectName("NavButton")
        self.btn_profile = QPushButton("Perfil")
        self.btn_profile.setObjectName("NavButton")
        self.btn_ia=QPushButton("Asistente Virtual")
        self.btn_ia.setObjectName("NavButton")
        self.btn_logout = QPushButton("Cerrar Sesión")
        self.btn_logout.setObjectName("NavButton")
        
        for b in (self.btn_home, self.btn_modules, self.btn_simuladores, self.btn_ia, self.btn_profile):
            h.addWidget(b)
        
        h.addStretch()
        h.addWidget(self.btn_logout)
        root_l.addWidget(nav)

        self.stack = QStackedWidget()
        
        self.pagina_home = PaginaHome(ir_a_modulo_callback=self.navegar_a_modulo)
        self.pagina_perfil = PaginaPerfil()
        self.pagina_modulos = PaginaModulos()
        self.pagina_prueba = ChatWindow()
        self.pagina_simuladores = PaginaSimuladores()

        self.stack.addWidget(self.pagina_home)       
        self.stack.addWidget(self.pagina_modulos)     
        self.stack.addWidget(self.pagina_perfil)   
        self.stack.addWidget(self.pagina_prueba) 
        self.stack.addWidget(self.pagina_simuladores)

        root_l.addWidget(self.stack)
        self.setCentralWidget(root)

        self.btn_home.clicked.connect(self.ir_inicio)
        self.btn_profile.clicked.connect(self.ir_perfil)
        self.btn_modules.clicked.connect(self.ir_modulos)
        self.btn_logout.clicked.connect(self.logout)
        self.btn_ia.clicked.connect(self.ir_ia)
        self.btn_simuladores.clicked.connect(self.ir_simuladores)

    def ir_inicio(self):
        self.stack.setCurrentIndex(0)

    def ir_modulos(self):
        self.stack.setCurrentIndex(1)
        self.pagina_modulos.mostrar_lista_modulos()

    def ir_perfil(self):
        self.stack.setCurrentIndex(2)
    
    def ir_ia(self):
        self.stack.setCurrentIndex(3)

    def ir_simuladores(self):
        self.stack.setCurrentIndex(4)
        self.pagina_simuladores.mostrar_lista_simuladores()

    def navegar_a_modulo(self, nombre_modulo: str):
        self.stack.setCurrentIndex(1)  
        indice = self.pagina_modulos.nombre_modulos.index(nombre_modulo)
        self.pagina_modulos.modulo_clicado(indice)

    def logout(self):
        from Paginas.Login import VentanaLogin
        self.close()
        self.login = VentanaLogin()
        self.login.show()

