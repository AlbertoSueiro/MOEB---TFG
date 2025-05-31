import sys
from PySide6.QtWidgets import QApplication
from Paginas.Login import VentanaLogin
from Util.bbdd import iniciar_base_datos

if __name__ == "__main__":
    try:
        iniciar_base_datos()
    except Exception as e:
        print(e)
        
    app = QApplication(sys.argv)
    login = VentanaLogin(app)
    login.show()
    sys.exit(app.exec())
