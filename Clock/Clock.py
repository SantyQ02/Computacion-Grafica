import gi
gi.require_version('GooCanvas', '2.0')
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GooCanvas
import math

class SpiralApp:
    def __init__(self, radius, separation):
        # Crear una ventana
        self.window = Gtk.Window()
        self.window.set_title("Espiral de Arquímedes")
        self.window.set_default_size(600, 600)

        # Crear un canvas
        self.canvas = GooCanvas.Canvas()
        self.root = self.canvas.get_root_item()
        self.window.add(self.canvas)

        # Dibujar la espiral
        self.draw_archimedean_spiral(radius, separation)

        # Mostrar la ventana
        self.window.connect("destroy", Gtk.main_quit)
        self.window.show_all()

    def draw_archimedean_spiral(self, radius, separation):
        # Establecer el centro del canvas
        center_x = 300
        center_y = 300

        # Dibujar la espiral
        points = []
        for theta in range(0, 360 * 5):  # 5 vueltas
            rad = math.radians(theta)
            r = radius + separation * rad
            x = center_x + r * math.cos(rad)
            y = center_y + r * math.sin(rad)
            points.append((x, y))

        # Crear una línea en el canvas usando GooCanvas.CanvasPolyline
        points_object = GooCanvas.CanvasPoints.new(len(points))

        # Asignar los puntos de la lista a points_object
        for i, (x, y) in enumerate(points):
            points_object.set_point(i, x, y)

        # Crear la línea en el canvas
        line = GooCanvas.CanvasPolyline(
            parent=self.root,  # El objeto raíz del canvas
            points=points_object,
            stroke_color="black",  # Color de la línea
            line_width=2           # Ancho de la línea
        )

        # Dibujar círculos en los puntos
        for (x, y) in points:
            GooCanvas.CanvasItem.new(self.canvas, GooCanvas.Ellipse, {
                'x': x - 5,
                'y': y - 5,
                'width': 10,
                'height': 10,
                'fill_color': 'red',
            })

# Ejecutar la aplicación
if __name__ == "__main__":
    SpiralApp(radius=5, separation=1)
    Gtk.main()