import gi

gi.require_version("Gtk", "3.0")
from povview_utils import setup_goocanvas

setup_goocanvas()
from gi.repository import Gtk, GooCanvas, GdkPixbuf

from main_menu import Main_menu
from povview_things import Cone, Ovus
from povview_parser import parse
from povview_tracer import Tracer


TEST_CONE = {
    "type": "cone",
    "top_center": [0, 0, 0],
    "top_radius": 100.0,
    "bottom_center": [0, -150, 0],
    "bottom_radius": 50.0,
    "object_modifiers": [],
}
TEST_OVUS = {
    "type": "ovus",
    "bottom_radius": 100.0,
    "top_radius": 150.0,
    "object_modifiers": [],
}

COLORS = {
    "White": (1, 1, 1),
    "Black": (0, 0, 0),
    "Red": (1, 0, 0),
    "Green": (0, 1, 0),
    "Blue": (0, 0, 1),
    "Yellow": (1, 1, 0),
    "Orange": (1, 0.5, 0),
    "Cyan": (0, 1, 1),
    "Purple": (1, 0, 1),
}


class Views(Gtk.Grid):
    def __init__(self):
        super().__init__(row_spacing=4, column_spacing=4, margin=4)

        self.objs = []

        self.views = {}
        for x, y, lbl in [(0, 0, "xy"), (1, 0, "zy"), (0, 1, "zx")]:
            frame = Gtk.Frame(label=lbl, label_xalign=0.04, hexpand=True, vexpand=True)
            frame.connect("size-allocate", self.on_frame_size_allocate)
            self.attach(frame, x, y, 1, 1)

            canvas = GooCanvas.Canvas(
                automatic_bounds=False, bounds_from_origin=False, bounds_padding=10
            )
            frame.add(canvas)
            self.views[lbl] = {"frame": frame, "canvas": canvas}

            # Block scroll events on the canvas
            canvas.connect("scroll-event", self.on_scroll_event)

        # Tracer view
        self.tracer_frame = Gtk.Frame(
            label="Tracer", label_xalign=0.04, hexpand=True, vexpand=True
        )
        self.tracer_frame.connect("size-allocate", self.on_frame_size_allocate)
        self.attach(self.tracer_frame, 1, 1, 1, 1)

    def on_scroll_event(self, widget, event):
        return True

    def on_frame_size_allocate(self, widget, allocation):
        self.frame_width = widget.get_allocated_width()
        self.frame_height = widget.get_allocated_height()
        self.center_canvases()

    def center_canvases(self):
        for view in self.views.values():
            canvas = view["canvas"]
            canvas.set_bounds(
                -self.frame_width / 2,
                -self.frame_height / 2,
                self.frame_width,
                self.frame_height,
            )

    def clear_views(self):
        for view in self.views:
            root = self.views[view]["canvas"].get_root_item()
            for i in range(root.get_n_children() - 1, -1, -1):
                root.get_child(i).remove()

    def full_clear_views(self):
        for view in self.views:
            root = self.views[view]["canvas"].get_root_item()
            for i in range(root.get_n_children() - 1, -1, -1):
                root.get_child(i).remove()
        self.objs.clear()

    def add_object(self, obj, **kwargs):
        if kwargs.get("subdiv"):
            obj.set_params(**kwargs)
        self.objs.append(obj)

    def draw_and_trace(self):
        if not len(self.objs):
            return

        for obj in self.objs:
            obj.draw_on(self.views)

        tracer = Tracer(self.objs, (self.frame_width, self.frame_height))

        pixbuf = GdkPixbuf.Pixbuf.new_from_file("tracer.png")
        image = Gtk.Image.new_from_pixbuf(pixbuf)
        for child in self.tracer_frame.get_children():
            self.tracer_frame.remove(child)
        self.tracer_frame.add(image)
        self.tracer_frame.show_all()


class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connect("destroy", lambda x: Gtk.main_quit())
        self.set_default_size(800, 600)

        mm = self.make_main_menu()

        self.updating_yaw = False
        self.updating_pitch = False
        self.updating_roll = False

        subdiv_label = Gtk.Label(label="SUBDIV")
        subdiv_label.set_xalign(0)
        self.subdiv_entry = Gtk.Entry(text="10")
        self.subdiv_entry.set_hexpand(True)
        self.subdiv_entry.connect("changed", self.on_params_changed)

        subdiv_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        subdiv_vbox.pack_start(subdiv_label, False, False, 0)
        subdiv_vbox.pack_start(self.subdiv_entry, False, False, 0)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        hbox.set_homogeneous(False)

        hbox.pack_start(subdiv_vbox, True, True, 0)

        self.views = Views()

        grid = Gtk.Grid(vexpand=True)
        grid.attach(mm, 0, 0, 2, 1)
        grid.attach(hbox, 0, 1, 2, 1)
        grid.attach(self.views, 0, 2, 2, 1)
        self.add(grid)
        self.show_all()
        self.maximize()

    def run(self):
        Gtk.main()

    def make_main_menu(self):
        mm = Main_menu(["_File", "_Tests"])
        mm.add_items_to(
            "_File",
            (
                ("Open POV file", self.on_open_pov_clicked),
                ("Clear scene", self.on_clear_clicked),
                ("Redraw", self.on_redraw_clicked),
                (None, None),
                ("_Quit", self.on_quit_clicked),
            ),
        )

        mm.add_items_to("_Tests", (("Add Cone to viewer", self.on_add_cone_clicked),))
        mm.add_items_to("_Tests", (("Add Ovus to viewer", self.on_add_ovus_clicked),))

        return mm

    def get_params(self):
        return {
            "subdiv": int(self.subdiv_entry.get_text()),
        }

    def on_params_changed(self, param):
        self.views.clear_views()
        for obj in self.views.objs:
            obj.set_params(**self.get_params())
        self.views.draw_and_trace()

    def on_add_cone_clicked(self, menuitem):
        self.views.full_clear_views()
        self.views.add_object(
            Cone(
                TEST_CONE,
                **self.get_params(),
            )
        )
        self.views.draw_and_trace()

    def on_add_ovus_clicked(self, menuitem):
        self.views.full_clear_views()
        self.views.add_object(
            Ovus(
                TEST_OVUS,
                **self.get_params(),
            )
        )
        self.views.draw_and_trace()

    def on_clear_clicked(self, menuitem):
        self.views.clear_views()

    def on_redraw_clicked(self, menuitem):
        self.views.clear_views()
        for obj in self.views.objs:
            obj.set_params(**self.get_params())
        self.views.draw_and_trace()

    def on_open_pov_clicked(self, menuitem):
        fc = Gtk.FileChooserDialog(action=Gtk.FileChooserAction.OPEN)
        fc.add_buttons(
            "Cancel", Gtk.ResponseType.CANCEL, "Open", Gtk.ResponseType.ACCEPT
        )

        for f_name, f_pattern in (
            ("POVday files (*.pov)", "*.pov"),
            ("All files (*)", "*"),
        ):
            filter = Gtk.FileFilter()
            filter.set_name(f_name)
            filter.add_pattern(f_pattern)
            fc.add_filter(filter)

        if fc.run() == Gtk.ResponseType.ACCEPT:
            self.file = fc.get_filename()
            print(self.file)

        fc.destroy()

        self.views.full_clear_views()

        parsed_file = parse(self.file)
        objects = parsed_file["objects"]

        for obj in objects:
            self.views.add_object(obj, **self.get_params())
        self.views.draw_and_trace()

    def on_quit_clicked(self, menuitem):
        Gtk.main_quit()


def main(args):
    mainwdw = MainWindow()
    mainwdw.run()

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))
