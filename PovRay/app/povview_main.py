#!/usr/bin/env python3


import gi

gi.require_version("Gtk", "3.0")
gi.require_version("GooCanvas", "3.0")
from gi.repository import Gtk, GooCanvas

from main_menu import Main_menu
from povview_things import Vec3, Cone, Ovus
from pdb import set_trace as st
from povview_parser import parse


TEST_CONE = {
    "type": "cone",
    "data": [[-13.0, 12.34, -20], 11, [-13.0, -23.34, -12.23], 2],
}
TEST_OVUS = {
    "type": "ovus",
    "bottom_radius": 100.0,
    "top_radius": 150.0,
    "color": {"r": 1.0, "g": 0.0, "b": 0.0},
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
            self.attach(frame, x, y, 1, 1)

            canvas = GooCanvas.Canvas(
                automatic_bounds=True, bounds_from_origin=False, bounds_padding=10
            )
            frame.add(canvas)
            self.views[lbl] = {"frame": frame, "canvas": canvas}

    def clear(self):
        for view in self.views:
            root = self.views[view]["canvas"].get_root_item()
            for i in range(root.get_n_children()):
                root.get_child(i).remove()

    def add_object(self, obj):
        match obj["type"]:
            case "cone":
                c = Cone(obj["data"])
                self.objs.append(c)
                c.draw_on(self.views)
            case "ovus":
                o = Ovus(obj)
                self.objs.append(o)
                o.draw_on(self.views)
            case _:
                raise ValueError(f"Unknown object type: {obj['type']}")


class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connect("destroy", lambda x: Gtk.main_quit())
        self.set_default_size(800, 600)

        mm = self.make_main_menu()

        cmd_entry = Gtk.Entry(text=TEST_OVUS, hexpand=True)
        cmd_entry.connect("activate", self.on_cmd_entry_activate)

        self.views = Views()

        grid = Gtk.Grid(vexpand=True)
        grid.attach(mm, 0, 0, 2, 1)
        grid.attach(cmd_entry, 0, 1, 2, 1)
        grid.attach(self.views, 0, 2, 2, 1)
        self.add(grid)
        self.show_all()

    def run(self):
        Gtk.main()

    def make_main_menu(self):
        mm = Main_menu(["_File", "_Tests", "_Help"])
        mm.add_items_to(
            "_File",
            (
                ("Open POV file", self.on_open_pov_clicked),
                ("Clear scene", self.on_clear_clicked),
                (None, None),
                ("_Quit", self.on_quit_clicked),
            ),
        )

        mm.add_items_to("_Tests", (("Add Cone to viewer", self.on_add_cone_clicked),))
        mm.add_items_to("_Tests", (("Add Ovus to viewer", self.on_add_ovus_clicked),))

        return mm

    def on_add_cone_clicked(self, menuitem):
        self.views.add_object(TEST_CONE)

    def on_add_ovus_clicked(self, menuitem):
        self.views.add_object(TEST_OVUS)

    def on_clear_clicked(self, menuitem):
        self.views.clear()

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

        self.views.clear()

        # TODO: Unhardcode this on the future
        self.object = parse(self.file)["objects"][0]
        self.views.add_object(self.object)

    def on_quit_clicked(self, menuitem):
        Gtk.main_quit()

    def on_cmd_entry_activate(self, entry):
        print("Command: ", entry.get_text())


def main(args):
    mainwdw = MainWindow()
    mainwdw.run()

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))
