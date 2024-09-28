import gi
import cairo
from datetime import datetime
gi.require_version('Gtk', '3.0')
gi.require_version('GooCanvas', '2.0')
from gi.repository import Gtk, GooCanvas, GObject

# Clase principal del Reloj
class MovingClock(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Moving self.clock")
        self.set_default_size(1000, 600)
        self.pixel_size = 20
        
        self.canvas = GooCanvas.Canvas()
        self.canvas.set_size_request(*self.get_size())
        self.add(self.canvas)

        self.root = self.canvas.get_root_item()

        self.draw_clock()
        self.connect("configure-event", self.on_configure_event)

        GObject.timeout_add(20, self.update_hour_and_minute)
        GObject.timeout_add(10, self.update_second_ten)
        GObject.timeout_add(1, self.update_second_unit)

    def on_configure_event(self, obj, tgt):
        self.canvas.set_size_request(*self.get_size())
        self.center_clock()

    def draw_clock(self):
        self.clock = GooCanvas.CanvasGroup(parent=self.root)
        
        digit_groups = list()
        for _ in range(6):
            digit_groups.append(GooCanvas.CanvasGroup(parent=self.clock))

        self.digit_bgs = list()
        self.separators = list()
        self.digit_bgs.append(self.create_digit_group(0, 0, self.pixel_size, digit_groups[0]))
        self.covering_grid_1 = self.create_custom_shape(0, 0, self.pixel_size, digit_groups[0])

        self.digit_bgs.append(self.create_digit_group(self.pixel_size * 4, 0, self.pixel_size, digit_groups[1]))
        self.covering_grid_2 = self.create_custom_shape(self.pixel_size * 4, 0, self.pixel_size, digit_groups[1])
        
        self.separators.append(self.create_separator(self.pixel_size * 8, self.pixel_size, self.pixel_size, self.clock))
        self.separators.append(self.create_separator(self.pixel_size * 8, self.pixel_size * 3, self.pixel_size, self.clock))
        
        self.digit_bgs.append(self.create_digit_group(self.pixel_size * 10, 0, self.pixel_size, digit_groups[2]))
        self.covering_grid_3 = self.create_custom_shape(self.pixel_size * 10, 0, self.pixel_size, digit_groups[2])
        
        self.digit_bgs.append(self.create_digit_group(self.pixel_size * 14, 0, self.pixel_size, digit_groups[3]))
        self.covering_grid_4 = self.create_custom_shape(self.pixel_size * 14, 0, self.pixel_size, digit_groups[3])
        
        self.separators.append(self.create_separator(self.pixel_size * 18, self.pixel_size, self.pixel_size, self.clock))
        self.separators.append(self.create_separator(self.pixel_size * 18, self.pixel_size * 3, self.pixel_size, self.clock))
        
        self.digit_bgs.append(self.create_digit_group(self.pixel_size * 20, 0, self.pixel_size, digit_groups[4]))
        self.covering_grid_5 = self.create_custom_shape(self.pixel_size * 20, 0, self.pixel_size, digit_groups[4])
        
        self.digit_bgs.append(self.create_digit_group(self.pixel_size * 24, 0, self.pixel_size, digit_groups[5]))
        self.covering_grid_6 = self.create_custom_shape(self.pixel_size * 24, 0, self.pixel_size, digit_groups[5])

        self.center_clock()

        self.update_hour_and_minute()

    def center_clock(self):
        # Center X
        window_width, window_height = self.get_size()
        clock_bounds = self.clock.get_bounds()
        matrix_x = cairo.Matrix()
        matrix_x.x0 = window_width/2 - (clock_bounds.x2-clock_bounds.x1)/2
        self.clock.set_transform(matrix_x)

        # Center Y
        matrix_y = cairo.Matrix()
        self.offset = window_height/2 - self.pixel_size * 2.5
        matrix_y.y0 = self.offset
        for digit_bg in self.digit_bgs:
            digit_bg.set_transform(matrix_y)
        for separator in self.separators:
            separator.set_transform(matrix_y)

    def create_digit_group(self, x, y, pixel_size, parent_group):
        group = GooCanvas.CanvasGroup(parent=parent_group)
        for col in range(3):
            for row in range(5):
                GooCanvas.CanvasRect(x=x + col * pixel_size, y=y + row * pixel_size, width=pixel_size, height=pixel_size,
                                     stroke_color="black", fill_color="orange", parent=group)
        return group

    def create_separator(self, x, y, pixel_size, parent_group):
        group = GooCanvas.CanvasGroup(parent=parent_group)
        GooCanvas.CanvasRect(x=x , y=y, width=pixel_size, height=pixel_size, stroke_color="black", fill_color="orange", parent=group)
        return group
    
    def create_custom_shape(self, start_x, start_y, pixel_size, parent_group):
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
        final_pos = self.pixel_size * final_pos + self.offset - 1
        current_pos = int(group.get_bounds().y1)

        if current_pos == final_pos:
            return
        
        if current_pos > final_pos:
            group.translate(0,-step)
        else:
            group.translate(0,step)

    def update_hour_and_minute(self):
        parsed_now = self.parse_time()
        self.set_number(self.covering_grid_1, parsed_now["hour"]["ten"], 1)
        self.set_number(self.covering_grid_2, parsed_now["hour"]["unit"], 1)
        self.set_number(self.covering_grid_3, parsed_now["minute"]["ten"], 1)
        self.set_number(self.covering_grid_4, parsed_now["minute"]["unit"], 1)
        return True

    def update_second_ten(self):
        parsed_now = self.parse_time()
        self.set_number(self.covering_grid_5, parsed_now["second"]["ten"], 1)
        return True

    def update_second_unit(self):
        parsed_now = self.parse_time()
        self.set_number(self.covering_grid_6, parsed_now["second"]["unit"], 1)
        return True


win = MovingClock()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()