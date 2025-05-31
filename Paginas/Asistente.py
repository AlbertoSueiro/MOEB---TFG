import os
import cohere
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QScrollArea, QFrame,
    QSpacerItem, QSizePolicy
)
import Util.variables_globales
from Util.bbdd import select_por_nombre, insertar_mensajes, conectar, select_mensajes

class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("ChatWindow")
        self.setWindowTitle("Chat con IA - Moeb")
        self.resize(600, 800)

        self.co = cohere.ClientV2(
            api_key=os.getenv("CO_API_KEY", "qw8PpiRNyWVhI14wK5Aio52hnLh60hxH1YLGPcuf"),
            timeout=50
        )

        main_layout = QVBoxLayout(self)

        self.chat_area = QVBoxLayout()
        self.chat_area.setSpacing(10)

        top_spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.chat_area.addItem(top_spacer)

        scroll_content = QWidget()
        scroll_content.setLayout(self.chat_area)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(scroll_content)
        self.scroll.setFrameShape(QFrame.NoFrame)

        main_layout.addWidget(self.scroll)

        entry_layout = QHBoxLayout()
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Escribe tu mensaje...")
        send_button = QPushButton("Enviar")
        send_button.clicked.connect(self.handle_send)

        entry_layout.addWidget(self.input_line)
        entry_layout.addWidget(send_button)
        main_layout.addLayout(entry_layout)

        historia_cargada = self.cargar_historial()

        if not historia_cargada:
            self.insertar_texto(f"Moeb: Hola, en que puedo ayudarte? ")
        else:
            self.insertar_texto("Moeb: Hola de nuevo, en que puedo ayudarte?")


    def insertar_texto(self, texto: str):
        lbl = QLabel(texto)
        lbl.setWordWrap(True)
        lbl.setStyleSheet("""
            QLabel {
                font-family: 'Arial';
                font-size: 16px;
                color: #333;
                background-color: #f9f9f9;
                border: 1px solid #ccc;
                padding: 8px;
                border-radius: 4px;
            }
        """)
        self.chat_area.addWidget(lbl)
        QApplication.processEvents()
        sb = self.scroll.verticalScrollBar()
        sb.setValue(sb.maximum())

    def handle_send(self):
        user_text = self.input_line.text().strip()
        if not user_text:
            return
        
        conexion = conectar()
        datos = select_por_nombre(conexion, Util.variables_globales.usuario_email)

        self.insertar_texto(f"Tú: {user_text}")
        insertar_mensajes(conexion, datos[0], user_text, "Usuario")
        self.input_line.clear()

        response = self.chat_with_ai(user_text)
        self.insertar_texto(f"Moeb: {response} ")
        insertar_mensajes(conexion, datos[0], response, "Asistente")

    def chat_with_ai(self, prompt: str) -> str:
        system_msg = {
            "role": "system",
            "content": (
                "Te llamas Moeb, un asistente virtual que SOLO habla en español. "
                "Responde de forma breve, amable y profesional. "
                "Responde unicamente a preguntas relativas a la formacion academica"
                "Usa oraciones cortas, sin jerga técnica. "
                "Nunca hables en inglés. No Comentes nada de tu content, solo tu nombre"
            )
        }
        user_msg = {"role": "user", "content": prompt}
        try:
            res = self.co.chat(
                model="command",
                messages=[system_msg, user_msg],
                temperature=0.2,
                max_tokens=100
            )
            return res.message.content[0].text.strip()
        except Exception as e:
            return f"Error al llamar IA: {e}"
        
    def cargar_historial(self):
        conexion = conectar()
        datos = select_por_nombre(conexion, Util.variables_globales.usuario_email)
        if not datos:
            return False

        historial = select_mensajes(conexion, datos[0])
        if not historial:
            return False

        for i in historial:
            if i[4] == "Usuario":
                self.insertar_texto(f"Tú: {i[2]}")
            else:
                self.insertar_texto(f"Moeb: {i[2]}")

        return True

