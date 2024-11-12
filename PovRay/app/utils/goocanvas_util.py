# goocanvas_util.py
import gi

def setup_goocanvas():
    try:
        gi.require_version("GooCanvas", "3.0")
    except ValueError:
        try:
            gi.require_version("GooCanvas", "2.0")
        except ValueError:
            raise ImportError("No se encontró ninguna versión compatible de GooCanvas.")
