import numpy as np
from PIL import Image
from math import tan, radians
from concurrent.futures import ProcessPoolExecutor, as_completed
from io import BytesIO

from povview_math import Vec3, Ray, HitList
from povview_utils import setup_goocanvas

setup_goocanvas()
from gi.repository import GooCanvas, GdkPixbuf


class Tracer:
    def __init__(self, objects, size=(512, 512)):
        self.objects = objects
        self.size = size
        self._img = None

        self.trace()

    def get_img(self):
        return self._img

    def ray_generator_row(self, y, w, h, loc, angle):
        width = abs(loc.z) * 2 * tan(radians(angle) / 2)
        pixel = width / w
        rays = []
        for x in range(w):
            cx = (x - (w / 2) + 0.5) * pixel
            cy = (y - (h / 2) + 0.5) * pixel
            direction = Vec3(cx - loc.x, cy - loc.y, -loc.z).normalized()
            rays.append(Ray(loc, direction))
        return rays

    def trace_row(self, y):
        w, h = self.size
        loc = Vec3(0, 0, -40)
        angle = 30

        rays = self.ray_generator_row(y, w, h, loc, angle)
        row_colors = []
        hitlist = HitList()
        max_distance = 1000

        for ray in rays:
            hitlist.clear()
            for obj in self.objects:
                hitlist.extend(obj.intersection(ray))
            if not hitlist.empty():
                hit = hitlist.nearest_hit()
                distance = hit.t
                intensity = max(0, 1 - (distance / max_distance))
                hit_color = hit.obj.color.as_rgb8()
                adjusted_color = (
                    int(hit_color[0] * intensity),
                    int(hit_color[1] * intensity),
                    int(hit_color[2] * intensity),
                )
                row_colors.append(adjusted_color)
            else:
                row_colors.append((0, 0, 0))
        return y, row_colors

    def trace(self):
        w, h = self.size
        img_array = np.zeros((h, w, 3), dtype=np.uint8)

        with ProcessPoolExecutor() as executor:
            futures = {executor.submit(self.trace_row, y): y for y in range(h)}

            for future in as_completed(futures):
                y, row_colors = future.result()
                img_array[y, :] = row_colors

        self._img = Image.fromarray(img_array, "RGB")

    def draw_on(self, views, container_size):
        root = views["Tracer"]["canvas"].get_root_item()

        # Convert PIL Image to bytes using BytesIO
        buffer = BytesIO()
        self._img.save(buffer, format="PNG")
        buffer.seek(0)
        image_data = buffer.read()

        # Load pixbuf from bytes using PixbufLoader
        loader = GdkPixbuf.PixbufLoader.new_with_type("png")
        try:
            loader.write(image_data)
            loader.close()
            pixbuf = loader.get_pixbuf()
        except Exception as e:
            print(f"Error loading pixbuf from in-memory data: {e}")
            return

        # Original image dimensions
        img_width = pixbuf.get_width()
        img_height = pixbuf.get_height()

        # Container dimensions
        container_width, container_height = container_size

        # Calculate aspect ratios
        img_aspect = img_width / img_height
        container_aspect = container_width / container_height

        # Determine scaling factor to maintain aspect ratio
        if img_aspect > container_aspect:
            # Image is wider relative to container
            scale_width = container_width
            scale_height = int(container_width / img_aspect)
        else:
            # Image is taller relative to container
            scale_height = container_height
            scale_width = int(container_height * img_aspect)

        # Scale the pixbuf while maintaining aspect ratio
        scaled_pixbuf = pixbuf.scale_simple(
            scale_width,
            scale_height,
            GdkPixbuf.InterpType.BILINEAR,
        )

        # Optional: Calculate position to center the image within the container
        x_pos = (container_width - scale_width) // 2
        y_pos = (container_height - scale_height) // 2

        # Add the scaled and centered image to the canvas
        GooCanvas.CanvasImage(
            parent=root,
            pixbuf=scaled_pixbuf,
            width=scaled_pixbuf.get_width(),
            height=scaled_pixbuf.get_height(),
            x=x_pos,
            y=y_pos,
        )
