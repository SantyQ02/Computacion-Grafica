import numpy as np
from PIL import Image
from math import tan, radians
from concurrent.futures import ProcessPoolExecutor, as_completed
from io import BytesIO

from povview_math import Vec3, Ray, HitList
from povview_things import LightSource, Camera, Object3D
from povview_utils import setup_goocanvas

setup_goocanvas()
from gi.repository import GooCanvas, GdkPixbuf


class Tracer:
    def __init__(
        self,
        lights: list[LightSource],
        camera: Camera,
        objects: list[Object3D],
        size=(512, 512),
    ):
        self.lights = lights
        self.camera = camera
        self.objects = objects
        self.size = size
        self._img = None

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
        loc = self.camera.location
        angle = self.camera.angle

        rays = self.ray_generator_row(y, w, h, loc, angle)
        row_colors = []
        hitlist = HitList()
        light_hitlist = HitList()

        for ray in rays:
            hitlist.clear()
            light_hitlist.clear()
            hit_color = (0, 0, 0)

            for obj in self.objects:
                hitlist.extend(obj.intersection(ray))

            if hitlist.empty():
                row_colors.append(hit_color)
                continue

            hit = hitlist.nearest_hit()
            hit_point = ray.origin + ray.direction * hit.t

            # TODO: Consider multiple lights
            for light in self.lights:
                light_dir = (hit_point - light.location).normalized()
                light_ray = Ray(light.location, light_dir)

                for obj in self.objects:
                    light_hitlist.extend(obj.intersection(light_ray))

                if light_hitlist.empty():
                    continue

                light_hit = light_hitlist.nearest_hit()
                light_hit_point = light_ray.origin + light_ray.direction * light_hit.t

                if light_hit_point.round(6) == hit_point.round(6):
                    # TODO: Consider how light color affects hit color
                    hit_color = hit.obj.color.as_rgb8()
                    break

            row_colors.append(hit_color)

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

        buffer = BytesIO()
        self._img.save(buffer, format="PNG")
        buffer.seek(0)
        image_data = buffer.read()

        loader = GdkPixbuf.PixbufLoader.new_with_type("png")
        try:
            loader.write(image_data)
            loader.close()
            pixbuf = loader.get_pixbuf()
        except Exception as e:
            print(f"Error loading pixbuf from in-memory data: {e}")
            return

        img_width = pixbuf.get_width()
        img_height = pixbuf.get_height()

        container_width, container_height = container_size

        img_aspect = img_width / img_height
        container_aspect = container_width / container_height

        if img_aspect > container_aspect:
            scale_width = container_width
            scale_height = int(container_width / img_aspect)
        else:
            scale_height = container_height
            scale_width = int(container_height * img_aspect)

        scaled_pixbuf = pixbuf.scale_simple(
            scale_width,
            scale_height,
            GdkPixbuf.InterpType.BILINEAR,
        )

        x_pos = (container_width - scale_width) // 2
        y_pos = (container_height - scale_height) // 2

        GooCanvas.CanvasImage(
            parent=root,
            pixbuf=scaled_pixbuf,
            width=scaled_pixbuf.get_width(),
            height=scaled_pixbuf.get_height(),
            x=x_pos,
            y=y_pos,
        )
