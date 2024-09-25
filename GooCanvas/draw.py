import gi

gi.require_version("Gtk", "3.0")
gi.require_version("GooCanvas", "3.0")
from gi.repository import Gtk, GooCanvas

PIXEL_SIZE = 12
X_SIZE = 50
Y_SIZE = 50
HIGHLIGHT_STROKE_COLOR = "Blue"
NORMAL_STROKE_COLOR = "Gray"
BACKGROUND_COLOR = "White"


class PixelEditor(Gtk.Frame):
    def __init__(self):
        super().__init__(label="Pixel Editor", margin=4)
        canvas = GooCanvas.Canvas()
        self.cvroot = canvas.get_root_item()

        for y in range(Y_SIZE):
            for x in range(X_SIZE):
                r = GooCanvas.CanvasRect(
                    parent=self.cvroot,
                    x=x * PIXEL_SIZE,
                    y=y * PIXEL_SIZE,
                    width=PIXEL_SIZE - 1,
                    height=PIXEL_SIZE - 1,
                    line_width=1,
                    stroke_color=NORMAL_STROKE_COLOR,
                    fill_color=BACKGROUND_COLOR,
                )

                r.connect("enter-notify-event", self.on_enter)
                r.connect("leave-notify-event", self.on_leave)
                r.connect("button-press-event", self.on_click)

        self.col_btn = Gtk.ColorButton()
        save_as_btn = Gtk.Button(label="Save as")
        save_as_btn.connect("clicked", self.save_image_as)

        vbox = Gtk.VBox()
        vbox.pack_start(self.col_btn, False, False, 0)
        vbox.pack_start(save_as_btn, False, False, 0)

        hbox = Gtk.HBox()
        hbox.pack_start(canvas, True, True, 0)
        hbox.pack_start(vbox, False, False, 0)
        self.add(hbox)

    def on_enter(self, rect, tgt, event):
        rect.set_property("stroke_color", HIGHLIGHT_STROKE_COLOR)

    def on_leave(self, rect, tgt, event):
        rect.set_property("stroke_color", NORMAL_STROKE_COLOR)

    def on_click(self, rect, tgt, event):
        rect.set_property("fill_color", self.col_btn.get_rgba().to_string())

    def save_image_as(self, filename):
        s = "P3\n" f"{X_SIZE} {Y_SIZE}\n" f"255\n"

        for nr in range(self.cvroot.get_n_children()):
            child = self.cvroot.get_child(nr)
            col = child.get_property("fill_color_rgba")
            col >>= 8

            s += f"{col >> 16:3d} {col >> 8 & 0xff:3d} {col & 0xff:3d}\n"

        with open(filename, "w") as f:
            f.write(s)

    def load_image(self):
        pass


class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connect("destroy", Gtk.main_quit)
        self.set_default_size(PIXEL_SIZE * (X_SIZE + 3), PIXEL_SIZE * Y_SIZE)
        self.set_resizable(False)

        self.add(PixelEditor())
        self.show_all()

    def run(self):
        Gtk.main()


def main(args):
    mainwdw = MainWindow()
    mainwdw.run()

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))
