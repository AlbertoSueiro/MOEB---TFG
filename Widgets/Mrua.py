from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt, QTimer, QPointF

class WidgetMRUA(QWidget):
    def __init__(self):
        super().__init__()

        self.velocidad_inicial = 0.0
        self.aceleracion = 0.0
        self.t_max = 3.0  
        self.t_actual = 0.0

        self.setMinimumSize(400, 200)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(50)

    def set_parameters(self, velocidad_inicial, aceleracion):
        self.velocidad_inicial = velocidad_inicial
        self.aceleracion = aceleracion
        self._reiniciar_animacion()

    def set_tiempo(self, t_max):
        self.t_max = max(2.0, t_max)  
        self._reiniciar_animacion()

    def _reiniciar_animacion(self):
        self.t_actual = 0.0

    def tick(self):
        self.t_actual += 0.05
        if self.t_actual > self.t_max:
            return
        self.update()

    def paintEvent(self, e):
        ancho = self.width()
        alto = self.height()
        margen = 30

        pintor = QPainter(self)
        pintor.setRenderHint(QPainter.Antialiasing)

  
        escala_pos = 20 
        t = self.t_actual
        s = self.velocidad_inicial * t + 0.5 * self.aceleracion * t * t
        v = self.velocidad_inicial + self.aceleracion * t

        x_inf = s * escala_pos
        area_utile = ancho - 2*margen

        if x_inf < 0:
            offset = -x_inf
        elif x_inf > area_utile:
            offset = area_utile - x_inf
        else:
            offset = 0

        pen_ejes = QPen(Qt.black, 2)
        pintor.setPen(pen_ejes)
        eje_y = alto - margen
        pintor.drawLine(margen, eje_y, ancho - margen, eje_y)

        
        marca_central = int(round(s))
        radios = 10  
        inicio = marca_central - radios
        fin = marca_central + radios

        for i in range(inicio, fin+1):
            x_marca_inf = i * escala_pos
            x_marca = margen + x_marca_inf + offset
            if margen <= x_marca <= ancho - margen:
                pintor.drawLine(x_marca, eje_y, x_marca, eje_y + 5)
                if i % 2 == 0:
                    pintor.drawText(x_marca - 10, eje_y + 20, f"{i} m")

        x_obj = margen + x_inf + offset
        y_obj = eje_y
        radio = 10
        pen_bola = QPen(Qt.red, 2)
        pintor.setPen(pen_bola)
        pintor.setBrush(Qt.red)
        pintor.drawEllipse(int(x_obj - radio), int(y_obj - radio), radio*2, radio*2)
        pintor.drawText(int(x_obj + 15), int(y_obj - 10), f"v = {v:.2f} m/s")

        pintor.end()
