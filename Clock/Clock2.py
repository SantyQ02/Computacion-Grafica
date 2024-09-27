import gi
gi.require_version('GooCanvas', '2.0')
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GooCanvas
import math

class SpiralApp:
    def __init__(self, radius, separation, N, turns):
        self.window = Gtk.Window()
        self.window.set_title("Espiral de Arquímedes")
        self.window.set_default_size(600, 600)

        self.canvas = GooCanvas.Canvas()
        self.window.add(self.canvas)

        self.root = self.canvas.get_root_item()

        self.draw_archimedean_spiral(radius, separation, turns)

        self.draw_labels(radius, separation, N, turns)

        self.window.connect("destroy", Gtk.main_quit)
        self.window.show_all()

    def draw_archimedean_spiral(self, radius, separation, turns):
        self.center_x = 300
        self.center_y = 300

        points = []
        for theta in range(0, 360 * turns):
            rad = math.radians(theta)
            r = radius + separation * rad
            x = self.center_x + r * math.cos(rad)
            y = self.center_y + r * math.sin(rad)
            points.append((x, y))

        points_object = GooCanvas.CanvasPoints.new(len(points))

        for i, (x, y) in enumerate(points):
            points_object.set_point(i, x, y)

        line = GooCanvas.CanvasPolyline(
            parent=self.root,
            points=points_object,
            stroke_color="black",
            line_width=5
        )

    def draw_labels(self, radius, separation, n, amount_per_turn):
        for turn in range(1, n + 1):
            theta = 360 * turn
            rad = math.radians(theta)
            r = radius + separation * rad
            x = self.center_x + r * math.cos(rad)
            y = self.center_y + r * math.sin(rad)

            label = GooCanvas.CanvasText(
                parent=self.root,
                text=str(n),
                x=x,
                y=y,
                font="Sans 12",
                fill_color="red"
            )

if __name__ == "__main__":
    SpiralApp(radius=10, separation=15, n=12, amount_per_turn=6)
    Gtk.main()
