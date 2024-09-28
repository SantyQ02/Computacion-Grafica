import gi
import cairo
from datetime import datetime
from time import sleep

gi.require_version('Gtk', '3.0')
gi.require_version('GooCanvas', '2.0')
from gi.repository import Gtk, GooCanvas, GObject

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

        self.draw_clock()

        GObject.timeout_add(5, self.update_clock)

    def draw_clock(self):
        clock = GooCanvas.CanvasGroup(parent=self.root)
        
        digit1 = GooCanvas.CanvasGroup(parent=clock)
        digit2 = GooCanvas.CanvasGroup(parent=clock)
        digit3 = GooCanvas.CanvasGroup(parent=clock)
        digit4 = GooCanvas.CanvasGroup(parent=clock)
        digit5 = GooCanvas.CanvasGroup(parent=clock)
        digit6 = GooCanvas.CanvasGroup(parent=clock)

        self.create_digit_group(0, 0, self.pixel_size, digit1)
        self.covering_grid_1 = self.create_custom_shape(0, 0, self.pixel_size, digit1)

        self.create_digit_group(80, 0, self.pixel_size, digit2)
        self.covering_grid_2 = self.create_custom_shape(80, 0, self.pixel_size, digit2)
        
        self.create_separator(160, 20, self.pixel_size, clock)
        self.create_separator(160, 60, self.pixel_size, clock)
        
        self.create_digit_group(200, 0, self.pixel_size, digit3)
        self.covering_grid_3 = self.create_custom_shape(200, 0, self.pixel_size, digit3)
        
        self.create_digit_group(280, 0, self.pixel_size, digit4)
        self.covering_grid_4 = self.create_custom_shape(280, 0, self.pixel_size, digit4)
        
        self.create_separator(360, 20, self.pixel_size, clock)
        self.create_separator(360, 60, self.pixel_size, clock)
        
        self.create_digit_group(400, 0, self.pixel_size, digit5)
        self.covering_grid_5 = self.create_custom_shape(400, 0, self.pixel_size, digit5)
        
        self.create_digit_group(480, 0, self.pixel_size, digit6)
        self.covering_grid_6 = self.create_custom_shape(480, 0, self.pixel_size, digit6)

        window_width, window_height = self.get_size()
        clock_bounds = clock.get_bounds()
        matrix = cairo.Matrix()
        matrix.x0 = window_width/2 - (clock_bounds.x2-clock_bounds.x1)/2
        matrix.y0 = window_height/2
        clock.set_transform(matrix)

        self.update_clock()

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

    def set_number(self, group, number, step):
        if number == 0:
            self.transition(group, 0, step)
        elif number == 1:
            self.transition(group, -5, step)
        elif number == 2:
            self.transition(group, -12, step)
        elif number == 3:
            self.transition(group, -10, step)
        elif number == 4:
            self.transition(group, -2, step)
        elif number == 5:
            self.transition(group, -14, step)
        elif number == 6:
            self.transition(group, -18, step)
        elif number == 7:
            self.transition(group, -4, step)
        elif number == 8:
            self.transition(group, -20, step)
        elif number == 9:
            self.transition(group, -22, step)
        else:
            raise ValueError("No valid number was given")
    
    def parse_time(self):
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        second = now.second
        
        return {"hour": {"ten": hour//10, "unit": hour%10},"minute": {"ten": minute//10, "unit": minute%10},"second": {"ten": second//10, "unit": second%10}}

    def transition(self, group, final_pos, step):
        final_pos = (self.pixel_size * final_pos) + 300
        current_pos = int(group.get_bounds().y1)

        if current_pos == final_pos:
            return
        
        if current_pos > final_pos:
            group.translate(0,-step)
        else:
            group.translate(0,step)

    def update_clock(self):
        parsed_now = self.parse_time()
        self.set_number(self.covering_grid_1, parsed_now["hour"]["ten"], 1)
        self.set_number(self.covering_grid_2, parsed_now["hour"]["unit"], 1)
        self.set_number(self.covering_grid_3, parsed_now["minute"]["ten"], 1)
        self.set_number(self.covering_grid_4, parsed_now["minute"]["unit"], 1)
        self.set_number(self.covering_grid_5, parsed_now["second"]["ten"], 1)
        self.set_number(self.covering_grid_6, parsed_now["second"]["unit"], 1)

        return True


win = MovingClock(20)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()