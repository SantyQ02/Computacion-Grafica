import gi
import cairo
from datetime import datetime

gi.require_version("Gtk", "3.0")
gi.require_version("GooCanvas", "2.0")
from gi.repository import Gtk, GooCanvas, GObject


# Clase principal del Reloj
class MovingClock(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Moving self.clock")
        self.set_default_size(1000, 600)
        self.pixel_size = 20

        self.canvas = GooCanvas.Canvas()
        self.canvas.set_hexpand(True)
        self.canvas.set_vexpand(True)

        box = Gtk.Box()
        box.pack_start(self.canvas, True, True, 0)
        self.add(box)

        self.root = self.canvas.get_root_item()

        self.draw_clock()
        self.connect("configure-event", self.on_configure_event)

        GObject.timeout_add(20, self.update_hour_and_minute)
        GObject.timeout_add(1, self.update_second)

    def on_configure_event(self, obj, tgt):
        self.center_clock()
        return False

    def draw_clock(self):
        self.clock = GooCanvas.CanvasGroup(parent=self.root)

        digit_groups = list()
        for _ in range(6):
            digit_groups.append(GooCanvas.CanvasGroup(parent=self.clock))

        self.digit_bgs = list()
        self.separators = list()

        # Digit 1
        self.digit_bgs.append(
            self.create_digit_group(
                x=0, y=0, pixel_size=self.pixel_size, parent_group=digit_groups[0]
            )
        )
        self.covering_grid_1 = self.create_custom_shape(
            start_x=0,
            start_y=0,
            pixel_size=self.pixel_size,
            parent_group=digit_groups[0],
        )

        # Digit 2
        self.digit_bgs.append(
            self.create_digit_group(
                x=self.pixel_size * 4,
                y=0,
                pixel_size=self.pixel_size,
                parent_group=digit_groups[1],
            )
        )
        self.covering_grid_2 = self.create_custom_shape(
            start_x=self.pixel_size * 4,
            start_y=0,
            pixel_size=self.pixel_size,
            parent_group=digit_groups[1],
        )

        # Separator Group 1
        self.separators.append(
            self.create_separator_group(
                x=self.pixel_size * 8,
                y=self.pixel_size,
                pixel_size=self.pixel_size,
                parent_group=self.clock,
            )
        )

        # Digit 3
        self.digit_bgs.append(
            self.create_digit_group(
                x=self.pixel_size * 10,
                y=0,
                pixel_size=self.pixel_size,
                parent_group=digit_groups[2],
            )
        )
        self.covering_grid_3 = self.create_custom_shape(
            start_x=self.pixel_size * 10,
            start_y=0,
            pixel_size=self.pixel_size,
            parent_group=digit_groups[2],
        )

        # Digit 4
        self.digit_bgs.append(
            self.create_digit_group(
                x=self.pixel_size * 14,
                y=0,
                pixel_size=self.pixel_size,
                parent_group=digit_groups[3],
            )
        )
        self.covering_grid_4 = self.create_custom_shape(
            start_x=self.pixel_size * 14,
            start_y=0,
            pixel_size=self.pixel_size,
            parent_group=digit_groups[3],
        )

        # Separator Group 2
        self.separators.append(
            self.create_separator_group(
                x=self.pixel_size * 18,
                y=self.pixel_size,
                pixel_size=self.pixel_size,
                parent_group=self.clock,
            )
        )

        # Digit 5
        self.digit_bgs.append(
            self.create_digit_group(
                x=self.pixel_size * 20,
                y=0,
                pixel_size=self.pixel_size,
                parent_group=digit_groups[4],
            )
        )
        self.covering_grid_5 = self.create_custom_shape(
            start_x=self.pixel_size * 20,
            start_y=0,
            pixel_size=self.pixel_size,
            parent_group=digit_groups[4],
        )

        # Digit 6
        self.digit_bgs.append(
            self.create_digit_group(
                x=self.pixel_size * 24,
                y=0,
                pixel_size=self.pixel_size,
                parent_group=digit_groups[5],
            )
        )
        self.covering_grid_6 = self.create_custom_shape(
            start_x=self.pixel_size * 24,
            start_y=0,
            pixel_size=self.pixel_size,
            parent_group=digit_groups[5],
        )

        self.center_clock()
        self.initialize_clock()

    def center_clock(self):
        # Center X
        window_width, window_height = self.get_size()
        clock_bounds = self.clock.get_bounds()
        matrix_x = cairo.Matrix()
        matrix_x.x0 = window_width / 2 - (clock_bounds.x2 - clock_bounds.x1) / 2
        self.clock.set_transform(matrix_x)

        # Center Y
        matrix_y = cairo.Matrix()
        self.offset = window_height / 2 - self.pixel_size * 2.5
        matrix_y.y0 = self.offset
        for digit_bg in self.digit_bgs:
            digit_bg.set_transform(matrix_y)
        for separator in self.separators:
            separator.set_transform(matrix_y)

    def create_digit_group(self, *, x: int, y: int, pixel_size: int, parent_group):
        group = GooCanvas.CanvasGroup(parent=parent_group)
        for col in range(3):
            for row in range(5):
                GooCanvas.CanvasRect(
                    x=x + col * pixel_size,
                    y=y + row * pixel_size,
                    width=pixel_size,
                    height=pixel_size,
                    stroke_color="black",
                    fill_color="orange",
                    parent=group,
                )
        return group

    def create_separator_group(self, *, x: int, y: int, pixel_size: int, parent_group):
        group = GooCanvas.CanvasGroup(parent=parent_group)
        for i in [1, 3]:
            GooCanvas.CanvasRect(
                x=x,
                y=y * i,
                width=pixel_size,
                height=pixel_size,
                stroke_color="black",
                fill_color="orange",
                parent=group,
            )
        return group

    def create_custom_shape(
        self, *, start_x: int, start_y: int, pixel_size: int, parent_group
    ):
        black_cells = [
            (1, 1),
            (1, 2),
            (1, 3),
            (0, 5),
            (1, 5),
            (0, 6),
            (1, 6),
            (0, 7),
            (1, 7),
            (0, 8),
            (1, 8),
            (0, 9),
            (1, 9),
            (0, 11),
            (1, 11),
            (0, 13),
            (1, 13),
            (1, 15),
            (2, 15),
            (0, 17),
            (1, 17),
            (1, 19),
            (2, 19),
            (1, 21),
            (1, 23),
            (0, 25),
            (1, 25),
            (0, 26),
            (1, 26),
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
                        fill_color="black",
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

    def set_number(self, *, group, number: int, step: int):
        if number == 0:
            self.transition(group=group, final_pos=0, step=step)
        elif number == 1:
            self.transition(group=group, final_pos=-5, step=step)
        elif number == 2:
            self.transition(group=group, final_pos=-12, step=step)
        elif number == 3:
            self.transition(group=group, final_pos=-10, step=step)
        elif number == 4:
            self.transition(group=group, final_pos=-2, step=step)
        elif number == 5:
            self.transition(group=group, final_pos=-14, step=step)
        elif number == 6:
            self.transition(group=group, final_pos=-18, step=step)
        elif number == 7:
            self.transition(group=group, final_pos=-4, step=step)
        elif number == 8:
            self.transition(group=group, final_pos=-20, step=step)
        elif number == 9:
            self.transition(group=group, final_pos=-22, step=step)
        else:
            raise ValueError("No valid number was given")

    def transition(self, *, group, final_pos: int, step: int):
        final_pos = self.pixel_size * final_pos + self.offset - 1
        current_pos = int(group.get_bounds().y1)

        if current_pos == final_pos:
            return

        if current_pos > final_pos:
            group.translate(0, -step)
        else:
            group.translate(0, step)

    def parse_time(self):
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        second = now.second

        return {
            "hour": {"ten": hour // 10, "unit": hour % 10},
            "minute": {"ten": minute // 10, "unit": minute % 10},
            "second": {"ten": second // 10, "unit": second % 10},
        }

    def update_hour_and_minute(self):
        parsed_now = self.parse_time()
        self.set_number(
            group=self.covering_grid_1, number=parsed_now["hour"]["ten"], step=1
        )
        self.set_number(
            group=self.covering_grid_2, number=parsed_now["hour"]["unit"], step=1
        )
        self.set_number(
            group=self.covering_grid_3, number=parsed_now["minute"]["ten"], step=1
        )
        self.set_number(
            group=self.covering_grid_4, number=parsed_now["minute"]["unit"], step=1
        )
        return True

    def update_second(self):
        parsed_now = self.parse_time()
        self.set_number(
            group=self.covering_grid_5, number=parsed_now["second"]["ten"], step=1
        )
        self.set_number(
            group=self.covering_grid_6, number=parsed_now["second"]["unit"], step=1
        )
        return True

    def initialize_clock(self):
        parsed_now = self.parse_time()
        self.set_number(
            group=self.covering_grid_1, number=parsed_now["hour"]["ten"], step=1
        )
        self.set_number(
            group=self.covering_grid_2, number=parsed_now["hour"]["unit"], step=1
        )
        self.set_number(
            group=self.covering_grid_3, number=parsed_now["minute"]["ten"], step=1
        )
        self.set_number(
            group=self.covering_grid_4, number=parsed_now["minute"]["unit"], step=1
        )
        self.set_number(
            group=self.covering_grid_5, number=parsed_now["second"]["ten"], step=1
        )
        self.set_number(
            group=self.covering_grid_6, number=parsed_now["second"]["unit"], step=1
        )


if __name__ == "__main__":
    win = MovingClock()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
