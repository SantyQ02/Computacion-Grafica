import gi
gi.require_version('GooCanvas', '2.0')
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GooCanvas, GLib
import math
import cairo  # Importar cairo para crear matrices de transformación

class SpiralApp:
    def __init__(self, radius, separation, turns):
        # Crear una ventana
        self.window = Gtk.Window()
        self.window.set_title("Espiral de Arquímedes Rotante con Pelota")
        self.window.set_default_size(600, 600)

        # Crear un canvas
        self.canvas = GooCanvas.Canvas()
        self.window.add(self.canvas)

        # Obtener el root item del canvas
        self.root = self.canvas.get_root_item()

        # Crear un grupo para la espiral, que permitirá aplicar la rotación
        self.spiral_group = GooCanvas.CanvasGroup(parent=self.root)

        # Dibujar la espiral
        self.draw_archimedean_spiral(radius, separation, turns)

        # Inicializar la pelota
        self.ball_radius = 10
        self.ball_position_y = 590  # Posición inicial de la pelota
        self.ball = GooCanvas.CanvasEllipse(
            parent=self.root,
            x=300,  # Coordenada x del centro
            y=self.ball_position_y,  # Coordenada y del centro
            radius_x=self.ball_radius,  # Radio en x
            radius_y=self.ball_radius,  # Radio en y
            fill_color="red"  # Color de la pelota
        )

        # Iniciar la rotación continua y el movimiento de la pelota
        self.angle = 0
        GLib.timeout_add(50, self.update)  # Actualizar cada 50 ms

        # Mostrar la ventana
        self.window.connect("destroy", Gtk.main_quit)
        self.window.show_all()

    def draw_archimedean_spiral(self, radius, separation, turns):
        # Establecer el centro del canvas
        self.center_x = 300
        self.center_y = 300

        # Dibujar la espiral
        points = []
        for theta in range(0, 360 * turns):  # 'turns' vueltas completas
            rad = math.radians(theta)
            r = radius + separation * rad
            x = self.center_x + r * math.cos(rad)
            y = self.center_y + r * math.sin(rad)
            points.append((x, y))

        # Crear una línea en el canvas usando GooCanvas.CanvasPolyline
        points_object = GooCanvas.CanvasPoints.new(len(points))

        # Asignar los puntos de la lista a points_object
        for i, (x, y) in enumerate(points):
            points_object.set_point(i, x, y)

        # Crear la línea en el canvas dentro del grupo de la espiral
        line = GooCanvas.CanvasPolyline(
            parent=self.spiral_group,  # Agregar al grupo de la espiral
            points=points_object,
            stroke_color="black",  # Color de la línea
            line_width=5           # Ancho de la línea
        )

    def rotate_spiral(self):
        """Aplica una rotación a la espiral cada vez que se llama."""
        self.angle = (self.angle + 5) % 360  # Aumenta el ángulo de rotación
        
        # Crear una matriz de transformación usando cairo
        matrix = cairo.Matrix()
        matrix.translate(self.center_x, self.center_y)  # Trasladar al centro
        matrix.rotate(math.radians(self.angle))          # Rotar
        matrix.translate(-self.center_x, -self.center_y)  # Volver al origen

        # Aplicar la transformación
        self.spiral_group.set_transform(matrix)

    def update(self):
        """Actualiza la posición de la pelota y la espiral."""
        self.rotate_spiral()  # Rotar la espiral

        # Mover la pelota hacia arriba
        self.ball_position_y -= 1  # Mover la pelota hacia arriba
        self.ball.set_property('x', self.center_x - self.ball_radius)  # Ajustar la posición x
        self.ball.set_property('y', self.ball_position_y)  # Ajustar la posición y

        # Si la pelota sale del canvas, reiniciarla
        if self.ball_position_y + self.ball_radius * 2 < 0:
            self.ball_position_y = 590  # Reiniciar la posición de la pelota

        return True  # Mantiene el temporizador activo para la actualización

# Ejecutar la aplicación
if __name__ == "__main__":
    SpiralApp(radius=4, separation=7, turns=5)
    Gtk.main()
