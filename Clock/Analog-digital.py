import gi
import math
import time

gi.require_version("Gtk", "3.0")
gi.require_version("GooCanvas", "3.0")  # GooCanvas 3.0
from gi.repository import Gtk, GooCanvas, GObject, GLib

class AnalogClock(Gtk.Window):
    def __init__(self):
        super().__init__(title="Analog/Digital Clock")

        self.set_default_size(400, 400)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("destroy", Gtk.main_quit)

        # Crear una caja para contener el botón y el canvas
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.main_box)

        # Añadir el canvas
        self.canvas = GooCanvas.Canvas()
        self.canvas.set_size_request(400, 400)
        self.canvas.set_bounds(0, 0, 400, 400)
        self.root = self.canvas.get_root_item()
        self.main_box.pack_start(self.canvas, True, True, 0)

        # Añadir un botón para cambiar entre los modos
        self.button = Gtk.Button(label="Switch to Digital Mode")
        self.button.connect("clicked", self.switch_mode)
        self.main_box.pack_start(self.button, False, False, 0)

        # Variables de control
        self.analog_mode = True

        # Dibujar el fondo del reloj analógico por defecto
        self.draw_clock_face()

        # Actualizar cada segundo
        GLib.timeout_add(1000, self.update_clock)

    def draw_clock_face(self):
        """Dibuja el fondo del reloj analógico con las marcas para las horas"""
        self.clear_canvas()  # Limpiar el canvas
        GooCanvas.CanvasEllipse(
            parent=self.root,
            center_x=200, center_y=200, radius_x=180, radius_y=180,
            stroke_color="black", line_width=3
        )

        # Dibujar las marcas de las horas
        for i in range(12):
            angle = 2 * math.pi * i / 12
            x1 = 200 + 160 * math.sin(angle)
            y1 = 200 - 160 * math.cos(angle)
            x2 = 200 + 175 * math.sin(angle)
            y2 = 200 - 175 * math.cos(angle)

            GooCanvas.CanvasPath(
                parent=self.root,
                data=f"M {x1},{y1} L {x2},{y2}",
                stroke_color="black", line_width=3
            )

        # Inicializar las agujas con sombras
        self.hour_hand_shadow, self.hour_hand = self.add_hand_with_shadow(200, 200, 200, 120, 8, "black")
        self.minute_hand_shadow, self.minute_hand = self.add_hand_with_shadow(200, 200, 200, 80, 5, "black")
        self.second_hand_shadow, self.second_hand = self.add_hand_with_shadow(200, 200, 200, 60, 2, "red")

    def add_hand_with_shadow(self, x1, y1, x2, y2, width, color):
        """Agrega una aguja y su sombra correspondiente"""
        # Sombra desplazada
        shadow = GooCanvas.CanvasPath(
            parent=self.root,
            data=f"M {x1 + 3},{y1 + 3} L {x2 + 3},{y2 + 3}",
            stroke_color="gray", line_width=width
        )
        # Aguja original
        hand = GooCanvas.CanvasPath(
            parent=self.root,
            data=f"M {x1},{y1} L {x2},{y2}",
            stroke_color=color, line_width=width
        )
        return shadow, hand

    def update_clock(self):
        """Actualiza las posiciones de las agujas del reloj o muestra la hora digital"""
        if self.analog_mode:
            # Reloj analógico
            t = time.localtime()
            seconds = t.tm_sec
            minutes = t.tm_min
            hours = t.tm_hour % 12 + minutes / 60.0

            # Calcular los ángulos de las agujas
            second_angle = 2 * math.pi * seconds / 60
            minute_angle = 2 * math.pi * minutes / 60
            hour_angle = 2 * math.pi * hours / 12

            # Actualizar la aguja de los segundos
            self.update_hand_with_shadow(self.second_hand_shadow, self.second_hand, 200, 200, second_angle, 140)

            # Actualizar la aguja de los minutos
            self.update_hand_with_shadow(self.minute_hand_shadow, self.minute_hand, 200, 200, minute_angle, 120)

            # Actualizar la aguja de las horas
            self.update_hand_with_shadow(self.hour_hand_shadow, self.hour_hand, 200, 200, hour_angle, 80)
        else:
            # Modo digital
            self.display_digital_clock()

        return True

    def update_hand_with_shadow(self, shadow, hand, x1, y1, angle, length):
        """Actualiza la posición de una aguja y su sombra"""
        x2 = x1 + length * math.sin(angle)
        y2 = y1 - length * math.cos(angle)
        
        # Actualizar sombra (desplazada)
        shadow.set_property("data", f"M {x1 + 3},{y1 + 3} L {x2 + 3},{y2 + 3}")
        
        # Actualizar aguja
        hand.set_property("data", f"M {x1},{y1} L {x2},{y2}")

    def display_digital_clock(self):
        """Muestra la hora en formato digital"""
        self.clear_canvas()  # Limpiar el canvas antes de dibujar el modo digital
        current_time = time.strftime("%H:%M:%S", time.localtime())
        GooCanvas.CanvasText(
            parent=self.root,
            x=200, y=200,
            text=current_time,
            font="Sans 50",
            fill_color="black",
            anchor=GooCanvas.CanvasAnchorType.CENTER
        )

    def switch_mode(self, widget):
        """Alterna entre reloj analógico y digital"""
        self.analog_mode = not self.analog_mode
        if self.analog_mode:
            self.draw_clock_face()
            self.button.set_label("Switch to Digital Mode")
        else:
            self.display_digital_clock()
            self.button.set_label("Switch to Analog Mode")

    def clear_canvas(self):
        """Limpia el canvas para cambiar entre modos"""
        num_children = self.root.get_n_children()
        for _ in range(num_children):
            child = self.root.get_child(0)  # Siempre eliminar el primero
            child.remove()

if __name__ == "__main__":
    win = AnalogClock()
    win.show_all()
    Gtk.main()