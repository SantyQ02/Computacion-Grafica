#!/usr/bin/env python3


import gi

gi.require_version("Gtk", "3.0")
gi.require_version("GooCanvas", "3.0")
from gi.repository import Gtk, Gdk, GooCanvas

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
        self.unique_obj = None

        self.views = {}
        for x, y, lbl in [(0, 0, "xy"), (1, 0, "zy"), (0, 1, "zx")]:
            frame = Gtk.Frame(label=lbl, label_xalign=0.04, hexpand=True, vexpand=True)
            self.attach(frame, x, y, 1, 1)

            canvas = GooCanvas.Canvas(
                automatic_bounds=True, bounds_from_origin=False, bounds_padding=10
            )
            frame.add(canvas)
            self.views[lbl] = {"frame": frame, "canvas": canvas}

    def clear_views(self):
        for view in self.views:
            root = self.views[view]["canvas"].get_root_item()
            for i in range(root.get_n_children()):
                root.get_child(i).remove()

    def clear_objects(self):
        self.objs = []

    def set_object(self, obj, **kwargs):
        match obj["type"]:
            case "cone":
                self.unique_obj = Cone(obj["data"], **kwargs)
            case "ovus":
                self.unique_obj = Ovus(obj, **kwargs)
            case _:
                raise ValueError(f"Unknown object type: {obj['type']}")

    def draw(self):
        self.unique_obj.draw_on(self.views)

    def add_object(self, obj, **kwargs):
        match obj["type"]:
            case "cone":
                c = Cone(obj["data"], **kwargs)
                self.objs.append(c)
            case "ovus":
                o = Ovus(obj, **kwargs)
                self.objs.append(o)
            case _:
                raise ValueError(f"Unknown object type: {obj['type']}")

    def draw_objects(self):
        for obj in self.objs:
            obj.draw_on(self.views)


class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connect("destroy", lambda x: Gtk.main_quit())
        self.set_default_size(800, 600)

        mm = self.make_main_menu()

        self.updating_yaw = False
        self.updating_pitch = False
        self.updating_roll = False

        # Existing Labels and Entries
        label_circular = Gtk.Label(label="CIRCULAR_SUBDIV")
        label_circular.set_xalign(0)
        self.entry_circular = Gtk.Entry(text="100")
        self.entry_circular.set_hexpand(True)
        self.entry_circular.connect("changed", self.on_params_changed)

        label_vertical = Gtk.Label(label="VERTICAL_SUBDIV")
        label_vertical.set_xalign(0)
        self.entry_vertical = Gtk.Entry(text="100")
        self.entry_vertical.set_hexpand(True)
        self.entry_vertical.connect("changed", self.on_params_changed)

        self.checkbox_squared = Gtk.CheckButton(label="SQUARED")
        self.checkbox_squared.connect("toggled", self.on_params_changed)

        # Yaw
        label_yaw = Gtk.Label(label="YAW")
        label_yaw.set_xalign(0)
        self.entry_yaw = Gtk.Entry(text="0")
        self.entry_yaw.set_hexpand(True)
        self.entry_yaw.connect("changed", self.on_params_changed)
        self.entry_yaw.connect("focus-out-event", self.on_entry_yaw_focus_out)

        # Create Scale for YAW
        adjustment_yaw = Gtk.Adjustment(
            value=0, lower=-180, upper=180, step_increment=1, page_increment=10
        )
        self.scale_yaw = Gtk.Scale(
            orientation=Gtk.Orientation.HORIZONTAL, adjustment=adjustment_yaw
        )
        self.scale_yaw.set_digits(0)
        self.scale_yaw.set_hexpand(True)
        self.scale_yaw.connect("value-changed", self.on_scale_yaw_changed)

        # Pitch
        label_pitch = Gtk.Label(label="PITCH")
        label_pitch.set_xalign(0)
        self.entry_pitch = Gtk.Entry(text="0")
        self.entry_pitch.set_hexpand(True)
        self.entry_pitch.connect("changed", self.on_params_changed)
        self.entry_pitch.connect("focus-out-event", self.on_entry_pitch_focus_out)

        # Create Scale for PITCH
        adjustment_pitch = Gtk.Adjustment(
            value=0, lower=-90, upper=90, step_increment=1, page_increment=10
        )
        self.scale_pitch = Gtk.Scale(
            orientation=Gtk.Orientation.HORIZONTAL, adjustment=adjustment_pitch
        )
        self.scale_pitch.set_digits(0)
        self.scale_pitch.set_hexpand(True)
        self.scale_pitch.connect("value-changed", self.on_scale_pitch_changed)

        # Roll
        label_roll = Gtk.Label(label="ROLL")
        label_roll.set_xalign(0)
        self.entry_roll = Gtk.Entry(text="0")
        self.entry_roll.set_hexpand(True)
        self.entry_roll.connect("changed", self.on_params_changed)
        self.entry_roll.connect("focus-out-event", self.on_entry_roll_focus_out)

        # Create Scale for ROLL
        adjustment_roll = Gtk.Adjustment(
            value=0, lower=-180, upper=180, step_increment=1, page_increment=10
        )
        self.scale_roll = Gtk.Scale(
            orientation=Gtk.Orientation.HORIZONTAL, adjustment=adjustment_roll
        )
        self.scale_roll.set_digits(0)
        self.scale_roll.set_hexpand(True)
        self.scale_roll.connect("value-changed", self.on_scale_roll_changed)

        # Organize existing entries into vertical boxes
        vbox_circular = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        vbox_circular.pack_start(label_circular, False, False, 0)
        vbox_circular.pack_start(self.entry_circular, False, False, 0)

        vbox_vertical = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        vbox_vertical.pack_start(label_vertical, False, False, 0)
        vbox_vertical.pack_start(self.entry_vertical, False, False, 0)

        # Organize new entries and scales into vertical boxes
        vbox_yaw = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        vbox_yaw.pack_start(label_yaw, False, False, 0)
        vbox_yaw.pack_start(self.entry_yaw, False, False, 0)
        vbox_yaw.pack_start(self.scale_yaw, False, False, 0)

        vbox_pitch = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        vbox_pitch.pack_start(label_pitch, False, False, 0)
        vbox_pitch.pack_start(self.entry_pitch, False, False, 0)
        vbox_pitch.pack_start(self.scale_pitch, False, False, 0)

        vbox_roll = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        vbox_roll.pack_start(label_roll, False, False, 0)
        vbox_roll.pack_start(self.entry_roll, False, False, 0)
        vbox_roll.pack_start(self.scale_roll, False, False, 0)

        # Create the main horizontal box and pack all vertical boxes
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        hbox.set_homogeneous(False)

        hbox.pack_start(vbox_circular, True, True, 0)
        hbox.pack_start(vbox_vertical, True, True, 0)
        hbox.pack_start(vbox_roll, True, True, 0)
        hbox.pack_start(vbox_pitch, True, True, 0)
        hbox.pack_start(vbox_yaw, True, True, 0)
        hbox.pack_start(self.checkbox_squared, False, False, 0)

        self.views = Views()

        grid = Gtk.Grid(vexpand=True)
        grid.attach(mm, 0, 0, 2, 1)
        grid.attach(hbox, 0, 1, 2, 1)
        grid.attach(self.views, 0, 2, 2, 1)
        self.add(grid)
        self.show_all()

    def on_scale_yaw_changed(self, scale):
        value = scale.get_value()
        self.entry_yaw.set_text(str(int(value)))

    def on_scale_pitch_changed(self, scale):
        value = scale.get_value()
        self.entry_pitch.set_text(str(int(value)))

    def on_scale_roll_changed(self, scale):
        value = scale.get_value()
        self.entry_roll.set_text(str(int(value)))

    def on_params_changed(self, param):
        self.views.clear_views()
        self.views.unique_obj.set_params(**self.get_params())
        self.views.draw()

    def on_entry_yaw_focus_out(self, entry, event):
        print(entry.get_text())
        if self.updating_yaw:
            return
        self.updating_yaw = True
        text = entry.get_text()
        try:
            value = int(text)
            entry.override_background_color(Gtk.StateFlags.NORMAL, None)
        except ValueError:
            rgba = Gdk.RGBA(1, 0, 0, 0.3)
            entry.override_background_color(Gtk.StateFlags.NORMAL, rgba)
            value = int(self.scale_yaw.get_value())
            entry.set_text(str(value))
            self.updating_yaw = False
            return

        adjustment = self.scale_yaw.get_adjustment()
        value = max(
            int(adjustment.get_lower()), min(int(adjustment.get_upper()), value)
        )

        self.scale_yaw.set_value(value)
        self.updating_yaw = False

    def on_entry_pitch_focus_out(self, entry, event):
        if self.updating_pitch:
            return
        self.updating_pitch = True
        text = entry.get_text()
        try:
            value = int(text)
            entry.override_background_color(Gtk.StateFlags.NORMAL, None)
        except ValueError:
            rgba = Gdk.RGBA(1, 0, 0, 0.3)
            entry.override_background_color(Gtk.StateFlags.NORMAL, rgba)
            value = int(self.scale_pitch.get_value())
            entry.set_text(str(value))
            self.updating_pitch = False
            return

        adjustment = self.scale_pitch.get_adjustment()
        value = max(
            int(adjustment.get_lower()), min(int(adjustment.get_upper()), value)
        )

        self.scale_pitch.set_value(value)
        self.updating_pitch = False

    def on_entry_roll_focus_out(self, entry, event):
        if self.updating_roll:
            return
        self.updating_roll = True
        text = entry.get_text()
        try:
            value = int(text)
            entry.override_background_color(Gtk.StateFlags.NORMAL, None)
        except ValueError:
            rgba = Gdk.RGBA(1, 0, 0, 0.3)
            entry.override_background_color(Gtk.StateFlags.NORMAL, rgba)
            value = int(self.scale_roll.get_value())
            entry.set_text(str(value))
            self.updating_roll = False
            return

        adjustment = self.scale_roll.get_adjustment()
        value = max(
            int(adjustment.get_lower()), min(int(adjustment.get_upper()), value)
        )

        self.scale_roll.set_value(value)
        self.updating_roll = False

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
            "CIRCULAR_SUBDIV": int(self.entry_circular.get_text()),
            "VERTICAL_SUBDIV": int(self.entry_vertical.get_text()),
            "ROTATION_VECTOR": [
                float(self.entry_roll.get_text()),
                float(self.entry_pitch.get_text()),
                float(self.entry_yaw.get_text()),
            ],
            "SQUARED": self.checkbox_squared.get_active(),
        }

    def on_add_cone_clicked(self, menuitem):
        self.views.clear_views()
        self.views.set_object(
            TEST_CONE,
            **self.get_params(),
        )
        self.views.draw()

    def on_add_ovus_clicked(self, menuitem):
        self.views.clear_views()
        self.views.set_object(
            TEST_OVUS,
            **self.get_params(),
        )
        self.views.draw()

    def on_clear_clicked(self, menuitem):
        self.views.clear_views()

    def on_redraw_clicked(self, menuitem):
        self.views.clear_views()
        self.views.unique_obj.set_params(**self.get_params())
        self.views.draw()

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

        self.views.clear_views()

        # TODO: Unhardcode this on the future
        self.object = parse(self.file)["objects"][0]
        self.views.set_object(self.object, **self.get_params())
        self.views.draw()

    def on_quit_clicked(self, menuitem):
        Gtk.main_quit()


def main(args):
    mainwdw = MainWindow()
    mainwdw.run()

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))
