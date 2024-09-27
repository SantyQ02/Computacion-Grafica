import gi
import math
import time

gi.require_version("Gtk", "3.0")
gi.require_version("GooCanvas", "3.0")
from gi.repository import Gtk, GooCanvas, GObject, Gdk


class AnalogClock(Gtk.Window):
    def __init__(self, default_margin):
        super().__init__(title="Analog Clock")
        self.default_margin = default_margin
        self.set_default_size(400, 400)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("destroy", Gtk.main_quit)

        # Crear el canvas
        self.canvas = GooCanvas.Canvas()
        self.canvas.set_size_request(400, 400)
        self.canvas.set_bounds(0, 0, 400, 400)

        self.root = self.canvas.get_root_item()
        self.add(self.canvas)

        # Dibujar el fondo del reloj
        self.connect("configure-event", self.on_configure_event)

        # Inicializar las agujas
        self.hour_hand_shadow, self.hour_hand = None, None
        self.minute_hand_shadow, self.minute_hand = None, None
        self.second_hand_shadow, self.second_hand = None, None

        # Actualizar cada segundo
        GObject.timeout_add(1000, self.update_clock)

    def on_configure_event(self, widget, event):
        """Redibuja el fondo del reloj cuando se cambia el tamaño de la ventana."""
        self.draw_clock_face()

    def draw_clock_face(self):
        """Dibuja el fondo del reloj con las marcas para las horas."""
        self.clear_canvas()

        width, height = self.get_size()
        radius = min(height, width) / 2 - self.default_margin

        GooCanvas.CanvasEllipse(
            parent=self.root,
            center_x=width / 2,
            center_y=height / 2,
            radius_x=radius,
            radius_y=radius,
            stroke_color="black",
            line_width=3,
        )

        # Dibujar las marcas de las horas
        for i in range(12):
            angle = 2 * math.pi * i / 12
            x1 = width / 2 + (radius - 20) * math.sin(angle)
            y1 = height / 2 - (radius - 20) * math.cos(angle)
            x2 = width / 2 + (radius - 40) * math.sin(angle)
            y2 = height / 2 - (radius - 40) * math.cos(angle)

            GooCanvas.CanvasPath(
                parent=self.root,
                data=f"M {x1},{y1} L {x2},{y2}",
                stroke_color="black",
                line_width=3,
            )

        # Inicializar las agujas con sombras
        self.hour_hand_shadow, self.hour_hand = self.add_hand_with_shadow(
            width / 2, height / 2, width / 2, height / 2 - 80, 8, "black"
        )
        self.minute_hand_shadow, self.minute_hand = self.add_hand_with_shadow(
            width / 2, height / 2, width / 2, height / 2 - 60, 5, "black"
        )
        self.second_hand_shadow, self.second_hand = self.add_hand_with_shadow(
            width / 2, height / 2, width / 2, height / 2 - 40, 2, "red"
        )

    def clear_canvas(self):
        """Clear the canvas and redraw the background."""
        self.canvas.remove_all()

    def add_hand_with_shadow(self, x1, y1, x2, y2, width, color):
        """Agrega una aguja y su sombra correspondiente."""
        shadow = GooCanvas.CanvasPath(
            parent=self.root,
            data=f"M {x1 + 3},{y1 + 3} L {x2 + 3},{y2 + 3}",
            stroke_color="gray",
            line_width=width,
        )
        hand = GooCanvas.CanvasPath(
            parent=self.root,
            data=f"M {x1},{y1} L {x2},{y2}",
            stroke_color=color,
            line_width=width,
        )
        return shadow, hand

    def update_clock(self):
        """Actualiza las posiciones de las agujas del reloj."""
        t = time.localtime()
        seconds = t.tm_sec
        minutes = t.tm_min
        hours = t.tm_hour % 12 + minutes / 60.0

        # Calcular los ángulos de las agujas
        second_angle = 2 * math.pi * seconds / 60
        minute_angle = 2 * math.pi * minutes / 60
        hour_angle = 2 * math.pi * hours / 12

        # Actualizar la aguja de los segundos
        self.update_hand_with_shadow(
            self.second_hand_shadow, self.second_hand, 200, 200, second_angle, 140
        )

        # Actualizar la aguja de los minutos
        self.update_hand_with_shadow(
            self.minute_hand_shadow, self.minute_hand, 200, 200, minute_angle, 120
        )

        # Actualizar la aguja de las horas
        self.update_hand_with_shadow(
            self.hour_hand_shadow, self.hour_hand, 200, 200, hour_angle, 80
        )

        return True

    def update_hand_with_shadow(self, shadow, hand, x1, y1, angle, length):
        """Actualiza la posición de una aguja y su sombra."""
        x2 = x1 + length * math.sin(angle)
        y2 = y1 - length * math.cos(angle)

        shadow.set_property("data", f"M {x1 + 3},{y1 + 3} L {x2 + 3},{y2 + 3}")
        hand.set_property("data", f"M {x1},{y1} L {x2},{y2}")


if __name__ == "__main__":
    win = AnalogClock(default_margin=20)
    win.show_all()
    Gtk.main()