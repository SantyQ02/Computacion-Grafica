import numpy as np
from PIL import Image
from math import tan, radians
from concurrent.futures import ProcessPoolExecutor, as_completed

from povview_math import Vec3, Ray, HitList


class Tracer:
    def __init__(self, objects, size=(512, 512)):
        self.objects = objects
        self.size = size
        self._img = None

        self.trace()

    def get_img(self):
        return self._img

    def ray_generator_row(self, y, w, h, loc, angle):
        """
        Generador de rayos para una fila específica.
        """
        width = abs(loc.z) * 2 * tan(radians(angle) / 2)
        pixel = width / w
        rays = []
        for x in range(w):
            # Centrar las coordenadas
            cx = (x - (w / 2) + 0.5) * pixel
            cy = (y - (h / 2) + 0.5) * pixel
            direction = Vec3(cx - loc.x, cy - loc.y, -loc.z).normalized()
            rays.append(Ray(loc, direction))
        return rays

    def trace_row(self, y):
        """
        Procesa una fila completa de píxeles.
        """
        w, h = self.size
        loc = Vec3(0, 0, -40)
        angle = 30

        rays = self.ray_generator_row(y, w, h, loc, angle)
        row_colors = []
        hitlist = HitList()

        for ray in rays:
            hitlist.clear()
            for obj in self.objects:
                hitlist.extend(obj.intersection(ray))
            if not hitlist.empty():
                hit = hitlist.nearest_hit()
                hit_color = hit.obj.color.as_rgb8()
                row_colors.append(hit_color)
            else:
                # Color de fondo (negro)
                row_colors.append((0, 0, 0))
        return y, row_colors

    def trace(self):
        """
        Realiza el trazado de rayos en paralelo.
        """
        w, h = self.size
        img_array = np.zeros((h, w, 3), dtype=np.uint8)

        with ProcessPoolExecutor() as executor:
            # Enviar tareas para cada fila
            futures = {executor.submit(self.trace_row, y): y for y in range(h)}

            for future in as_completed(futures):
                y, row_colors = future.result()
                img_array[y, :] = row_colors

        # Crear la imagen a partir del array
        self._img = Image.fromarray(img_array, 'RGB')
        self._img.save("tracer.png")