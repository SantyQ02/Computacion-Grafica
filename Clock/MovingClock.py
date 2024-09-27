import gi
import time
import math
import cairo
from datetime import datetime

gi.require_version('Gtk', '3.0')
gi.require_version('GooCanvas', '2.0')
from gi.repository import Gtk, GooCanvas, Gdk, GLib

# Clase principal del Reloj
class MovingClock(Gtk.Window):
    def __init__(self, pixel_size):
        self.pixel_size = pixel_size

        Gtk.Window.__init__(self, title="Moving Clock")
        self.set_default_size(600, 600)

        self.canvas = GooCanvas.Canvas()
        self.canvas.set_size_request(600, 600)
        self.add(self.canvas)

        self.root = self.canvas.get_root_item()

        self.clock = GooCanvas.CanvasGroup(parent=self.root)
        
        self.digit1 = GooCanvas.CanvasGroup(parent=self.clock)
        self.digit2 = GooCanvas.CanvasGroup(parent=self.clock)
        self.digit3 = GooCanvas.CanvasGroup(parent=self.clock)
        self.digit4 = GooCanvas.CanvasGroup(parent=self.clock)

        self.hour1 = self.create_digit_group(0, 0, self.pixel_size, self.digit1)
        self.custom_shape = self.create_custom_shape(0, 0, self.pixel_size, self.digit1)
        self.set_number(self.custom_shape, 3)

        self.hour2 = self.create_digit_group(80, 0, self.pixel_size, self.digit2)
        self.custom_shape = self.create_custom_shape(80, 0, self.pixel_size, self.digit2)
        self.set_number(self.custom_shape, 3)
        
        self.separator1 = self.create_separator(160, 20, self.pixel_size, self.clock)
        self.separator2 = self.create_separator(160, 60, self.pixel_size, self.clock)
        
        self.minute1 = self.create_digit_group(200, 0, self.pixel_size, self.digit3)
        self.custom_shape = self.create_custom_shape(200, 0, self.pixel_size, self.digit3)
        self.set_number(self.custom_shape, 3)
        
        self.minute2 = self.create_digit_group(280, 0, self.pixel_size, self.digit4)
        self.custom_shape = self.create_custom_shape(280, 0, self.pixel_size, self.digit4)
        self.set_number(self.custom_shape, 3)

        window_width, window_height = self.get_size()
        clock_bounds = self.clock.get_bounds()
        matrix = cairo.Matrix()
        matrix.x0 = window_width/2 - (clock_bounds.x2-clock_bounds.x1)/2
        matrix.y0 = window_height/2
        # self.clock.set_simple_transform(window_width/2 - (clock_bounds.x2-clock_bounds.x1)/2, window_height/2, 1, 0)
        self.clock.set_transform(matrix)
        
    def create_digit_group(self, x, y, pixel_size, parent_group):
        """Crea un grupo de paneles en forma de dígito"""
        group = GooCanvas.CanvasGroup(parent=parent_group)
        for col in range(3):
            for row in range(5):
                GooCanvas.CanvasRect(x=x + col * pixel_size, y=y + row * pixel_size, width=pixel_size, height=pixel_size,
                                     stroke_color="black", fill_color="orange", parent=group)
        return group

    def create_separator(self, x, y, pixel_size, parent_group):
        """Crea los dos puntos separadores en el reloj"""
        group = GooCanvas.CanvasGroup(parent=parent_group)
        GooCanvas.CanvasRect(x=x , y=y, width=pixel_size, height=pixel_size, stroke_color="black", fill_color="orange", parent=group)
        return group
    
    def create_custom_shape(self, start_x, start_y, pixel_size, parent_group):
        """Crea un grupo con la forma de la imagen proporcionada"""
        black_cells = [
            (1, 1), 
            (1, 2), 
            (1, 3),
            (0, 5), (1, 5), 
            (0, 6), (1, 6), 
            (0, 7), (1, 7), 
            (0, 8), (1, 8), 
            (0, 9), (1, 9), 
            (0, 11), (1, 11),
            (0, 13), (1, 13), 
            (1, 15), (2, 15), 
            (0, 17), (1, 17), 
            (1, 19), (2, 19),
            (1, 21),
            (1, 23),
            (0, 25), (1, 25),
            (0, 26), (1, 26),
        ]

        group = GooCanvas.CanvasGroup(parent=parent_group)

        for col in range(3):
            for row in range(26):
                if (col, row) in black_cells:
                    GooCanvas.CanvasRect(
                        parent=group,
                        x=start_x + col * pixel_size,
                        y=start_y + row * pixel_size,
                        width=pixel_size,
                        height=pixel_size,
                        stroke_color="black",
                        fill_color="black"
                    )
                else:
                    GooCanvas.CanvasRect(
                        parent=group,
                        x=start_x + col * pixel_size,
                        y=start_y + row * pixel_size,
                        width=pixel_size,
                        height=pixel_size,
                        stroke_color="black",
                    )

        return group

    def set_number(self, group, number):
        if number == 0:
            matrix = cairo.Matrix()
            matrix.y0 = self.pixel_size * 0
            group.set_transform(matrix)
        elif number == 1:
            matrix = cairo.Matrix()
            matrix.y0 = self.pixel_size * -5
            group.set_transform(matrix)
        elif number == 2:
            matrix = cairo.Matrix()
            matrix.y0 = self.pixel_size * -12
            group.set_transform(matrix)
        elif number == 3:
            matrix = cairo.Matrix()
            matrix.y0 = self.pixel_size * -10
            group.set_transform(matrix)
        elif number == 4:
            matrix = cairo.Matrix()
            matrix.y0 = self.pixel_size * -2
            group.set_transform(matrix)
        elif number == 5:
            matrix = cairo.Matrix()
            matrix.y0 = self.pixel_size * -14
            group.set_transform(matrix)
        elif number == 6:
            matrix = cairo.Matrix()
            matrix.y0 = self.pixel_size * -18
            group.set_transform(matrix)
        elif number == 7:
            matrix = cairo.Matrix()
            matrix.y0 = self.pixel_size * -4
            group.set_transform(matrix)
        elif number == 8:
            matrix = cairo.Matrix()
            matrix.y0 = self.pixel_size * -20
            group.set_transform(matrix)
        elif number == 9:
            matrix = cairo.Matrix()
            matrix.y0 = self.pixel_size * -22
            group.set_transform(matrix)
        else:
            raise ValueError("No valid number was given")
        

win = MovingClock(20)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()