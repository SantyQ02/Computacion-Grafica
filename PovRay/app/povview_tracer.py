import numpy as np
from PIL import Image
from math import tan, radians, pi, log, cos, sqrt
from concurrent.futures import ProcessPoolExecutor, as_completed
from io import BytesIO
import random

from povview_math import Ray, HitList, Vec3, RGB
from povview_things import LightSource, Camera, Object3D
from povview_parser import parse
from povview_utils import setup_goocanvas, timer

setup_goocanvas()
from gi.repository import GooCanvas, GdkPixbuf

MAX_BOUNCES = 10
LIGHT_SOURCE_SIZE = 100
RAYS_CASTS_PER_PIXEL = 1


class Tracer:
    def __init__(
        self,
        lights: list[LightSource],
        camera: Camera,
        objects: list[Object3D],
        size=(512, 512),
    ):
        self.lights = lights
        for light in self.lights:
            light.corner1 *= Vec3(LIGHT_SOURCE_SIZE, 1, LIGHT_SOURCE_SIZE)
            light.corner2 *= Vec3(LIGHT_SOURCE_SIZE, 1, LIGHT_SOURCE_SIZE)
        self.camera = camera
        self.objects = objects
        self.objects.extend(self.lights)
        self.size = size
        self._img = None

    @staticmethod
    def sign(num):
        return (num > 0) - (num < 0)

    @staticmethod
    def random_value_normal_distribution():
        theta = 2 * pi * random.random()
        rho = sqrt(-2 * log(random.random()))
        return rho * cos(theta)

    @staticmethod
    def random_direction():
        x = Tracer.random_value_normal_distribution()
        y = Tracer.random_value_normal_distribution()
        z = Tracer.random_value_normal_distribution()
        return Vec3(x, y, z).normalized()

    @staticmethod
    def random_hemisphere_direction(normal):
        direction = Tracer.random_direction()
        return direction * Tracer.sign(direction.dot(normal))

    # TODO: Up vector is still inverted
    def ray_generator_row(self, y):
        w, h = self.size

        forward = (self.camera.look_at - self.camera.location).normalized()
        right = forward.cross(self.camera.up).normalized()
        up = self.camera.up.normalized()

        width = 2 * tan(radians(self.camera.angle) / 2)
        pixel_width = width / w

        rays = []
        cy = (y - (h / 2) + 0.5) * pixel_width
        for x in range(w):
            cx = (x - (w / 2) + 0.5) * pixel_width
            direction = (forward + right * cx + up * cy).normalized()
            ray = Ray(self.camera.location, direction)
            rays.append(ray)

        return rays

    def trace_row(self, y):
        rays = self.ray_generator_row(y)
        row_colors = []

        for x, ray in enumerate(rays):
            # seed = y * self.size[0] + x

            pixel_color = RGB(0)
            for _ in range(RAYS_CASTS_PER_PIXEL):
                pixel_color += self.trace(ray)
            pixel_color /= RAYS_CASTS_PER_PIXEL

            row_colors.append(pixel_color.as_rgb8())

        return y, row_colors

    # TODO: Fix this function
    def trace(self, ray):
        incoming_light = RGB(0)
        ray_color = RGB(1)

        for i in range(MAX_BOUNCES + 1):
            hit = self.ray_collision(ray)
            if hit is None:
                break

            print(f"Path tracing: {i + 1} - Object: {hit.obj}")
            ray.origin = ray.origin + ray.direction * hit.t
            ray.direction = (hit.normal + self.random_direction()).normalized()

            if isinstance(hit.obj, LightSource):
                incoming_light += hit.obj.color * ray_color
                break
            else:
                ray_color *= hit.obj.color

        return incoming_light

    def ray_collision(self, ray):
        hitlist = HitList()
        for obj in self.objects:
            hitlist.extend(obj.intersection(ray))

        if hitlist.empty():
            return None

        return hitlist.nearest_hit()

    @timer
    def trace_scene(self):
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

    def to_png(self, filename: str):
        if self._img is not None:
            try:
                self._img.save(filename, "PNG")
                print(f"Imagen guardada exitosamente en {filename}")
            except Exception as e:
                print(f"Error al guardar la imagen: {e}")
        else:
            raise ValueError(
                "La imagen no ha sido renderizada aún. Llama al método trace() primero."
            )


def main(args):
    parsed_file = parse(args[1])
    tracer = Tracer(
        parsed_file["lights"],
        parsed_file["cameras"][0],
        parsed_file["objects"],
        (800, 600),
    )
    tracer.trace_scene()
    tracer.to_png("tracer.png")


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))
