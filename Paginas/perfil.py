from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFileDialog, QSizePolicy, QSpacerItem)
from PySide6.QtCore import Qt, QMargins
from PySide6.QtGui import QPixmap, QPainter, QPainterPath
from Util.bbdd import conectar, modificar_nombre_usuario, modificar_password_usuario, select_por_nombre, insertar_imagen, eliminar_usuarios, select_imagen
import Util.variables_globales
from PySide6.QtGui import QPixmap
from Util.hash import hashear_pass


class PaginaPerfil(QWidget):
    def __init__(self, email_usuario=None, parent=None):
        super().__init__(parent)

        self.email_original = Util.variables_globales.usuario_email

        layout_principal = QHBoxLayout(self)
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(40)

        layout_izquierda = QVBoxLayout()
        layout_izquierda.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        layout_izquierda.setSpacing(15)

        label_titulo = QLabel("Tu Perfil")
        label_titulo.setAlignment(Qt.AlignCenter)
        label_titulo.setStyleSheet("font-size:22px; font-weight: bold; margin-bottom: 10px;")
        layout_izquierda.addWidget(label_titulo)

        self.label_imagen = QLabel()
        self.label_imagen.setFixedSize(150, 150)
        self.label_imagen.setAlignment(Qt.AlignCenter)
        self.label_imagen.setStyleSheet("border: 1px solid gray; border-radius: 75px;")
        layout_izquierda.addWidget(self.label_imagen, alignment=Qt.AlignCenter)

        self.btn_cargar_imagen = QPushButton("Cambiar imagen de perfil")
        layout_izquierda.addWidget(self.btn_cargar_imagen, alignment=Qt.AlignCenter)
        self.btn_cargar_imagen.clicked.connect(self.cargar_imagen_perfil)

        layout_izquierda.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout_principal.addLayout(layout_izquierda)

        layout_derecha = QVBoxLayout()
        layout_derecha.setSpacing(5)
        layout_derecha.setAlignment(Qt.AlignTop)

        layout_derecha.addSpacing(25)

        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Correo electrónico")
        self.input_email.setContentsMargins(QMargins(0, 0, 0, 3))
        layout_derecha.addWidget(self.input_email)

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Nueva contraseña")
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setContentsMargins(QMargins(0, 0, 0, 3))
        layout_derecha.addWidget(self.input_password)

        self.input_password_repeat = QLineEdit()
        self.input_password_repeat.setPlaceholderText("Repetir nueva contraseña")
        self.input_password_repeat.setEchoMode(QLineEdit.Password)
        self.input_password_repeat.setContentsMargins(QMargins(0, 0, 0, 10))
        layout_derecha.addWidget(self.input_password_repeat)

        botones_layout = QHBoxLayout()
        self.btn_guardar = QPushButton("Guardar Cambios")
        self.btn_borrar = QPushButton("Eliminar Cuenta")
        self.btn_borrar.setStyleSheet("background-color: #e74c3c; color: white;")
        botones_layout.addWidget(self.btn_guardar)
        botones_layout.addWidget(self.btn_borrar)
        layout_derecha.addLayout(botones_layout)

        layout_principal.addLayout(layout_derecha)

        layout_derecha.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))


        self.btn_guardar.clicked.connect(self.guardar_cambios)
        self.btn_borrar.clicked.connect(self.confirmar_borrado)

        self.imagen_path = None
        self.mostrar_imagen_perfil("")

        if self.email_original is not None:
            self.cargar_datos_usuario()


    def cargar_datos_usuario(self):
        conexion = conectar()
        if not conexion:
            QMessageBox.critical(self, "Error", "No se pudo conectar a la base de datos.")
            return

        try:
            usuario = select_por_nombre(conexion, self.email_original)
            if usuario:
                email = usuario[1]
                self.input_email.setText(email)

                img_data = select_imagen(conexion, email)
                if img_data:
                    pixmap = QPixmap()
                    if pixmap.loadFromData(img_data):  
                        scaled = pixmap.scaled(
                            self.label_imagen.width(),
                            self.label_imagen.height(),
                            Qt.KeepAspectRatioByExpanding,
                            Qt.SmoothTransformation
                        )
                        self.label_imagen.setPixmap(self.pixmap_circular(scaled))
                    else:
                        print("No se pudo cargar QPixmap desde los datos")
            else:
                print("Usuario no encontrado para cargar_datos_usuario")
        except Exception as e:
            print("Error", f"Error al cargar datos: {e}")
        finally:
            conexion.close()


    def mostrar_imagen_perfil(self, ruta_imagen):
        if ruta_imagen:
            pixmap = QPixmap(ruta_imagen)
            pixmap = pixmap.scaled(self.label_imagen.width(), self.label_imagen.height(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            pixmap_circular = self.pixmap_circular(pixmap)
            self.label_imagen.setPixmap(pixmap_circular)
        else:
            self.label_imagen.setPixmap(QPixmap())

    def pixmap_circular(self, pixmap):
        size = min(pixmap.width(), pixmap.height())
        circular_pixmap = QPixmap(size, size)
        circular_pixmap.fill(Qt.transparent)

        painter = QPainter(circular_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addEllipse(0, 0, size, size)
        painter.setClipPath(path)
        src_x = (pixmap.width() - size) // 2
        src_y = (pixmap.height() - size) // 2
        painter.drawPixmap(0, 0, pixmap.copy(src_x, src_y, size, size))
        painter.end()

        return circular_pixmap

    def cargar_imagen_perfil(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Seleccionar imagen de perfil", "","Imagenes (*.png *.jpg *.jpeg *.bmp *.gif)")
        if ruta:
            self.imagen_path = ruta
            self.mostrar_imagen_perfil(ruta)
            conexion = conectar()
            try:
                insertar_imagen(conexion, self.email_original, ruta)
                QMessageBox.information(self, "Exito", "Imagen de perfil actualizada correctamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al actualizar la imagen de perfil: {e}")
            finally:
                conexion.close()

            
    def guardar_cambios(self):
        email = self.input_email.text().strip()
        password = self.input_password.text()
        password_repeat = self.input_password_repeat.text()

        if not email:
            QMessageBox.warning(self, "Error", "El email es obligatorio.")
            return

        if password or password_repeat:
            if password != password_repeat:
                QMessageBox.warning(self, "Error", "Las contraseñas no coinciden.")
                return

        conexion = conectar()
        if not conexion:
            QMessageBox.critical(self, "Error", "No se pudo conectar a la base de datos.")
            return

        try:
            modificar_nombre_usuario(conexion, self.email_original, email)
            if password:
                
                modificar_password_usuario(conexion, email, hashear_pass(password))
            QMessageBox.information(self, "Guardado", "Tus cambios han sido guardados correctamente.")
            self.input_password.clear()
            self.input_password_repeat.clear()
            self.email_original = email  
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar cambios: {e}")
        finally:
            conexion.close()

    def confirmar_borrado(self):
        respuesta = QMessageBox.question(self, "Confirmar eliminación","¿Estás seguro de que quieres eliminar tu cuenta? Esta acción no se puede deshacer.", QMessageBox.Yes | QMessageBox.No)
        if respuesta == QMessageBox.Yes:
            conexion= conectar()
            eliminar_usuarios(conexion,self.email_original)
            QMessageBox.information(self, "Cuenta eliminada", "Tu cuenta ha sido eliminada.")

            from Paginas.Login import VentanaLogin
            self.ventana_inicio = VentanaLogin()
            self.ventana_inicio.show()
            self.window().close()
