import pylab as plt
import numpy as np
import io
from PIL import Image
from math import tan, radians, sqrt

from gi.repository import GdkPixbuf

from povview_math import Vec3, RGB, Ray, Hit, HitList


class Tracer:
    def __init__(self, objects, size=(512, 512)):
        self.objects = objects
        self._img = None

        self.trace(size)

    def get_img(self):
        return self._img

    def ray_generator(self, w, h, loc, angle):
        width = abs(loc.z) * 2 * tan(radians(angle) / 2)
        pixel = width / w

        for i in range(w * h):
            x = (i % w) - (w // 2) + 0.5
            y = (i // w) - (h // 2) + 0.5
            x *= pixel
            y *= pixel
            direction = Vec3(x - loc.x, y - loc.y, 0 - loc.z)

            yield Ray(loc, direction.normalized())

    # TODO: Add a progress bar
    def trace(self, size):
        img = Image.new("RGB", size, 0)

        raygen = self.ray_generator(*size, Vec3(0, 0, -40), 30)
        hitlist = HitList()

        for i, ray in enumerate(raygen):
            hitlist.clear()
            x, y = i % size[0], i // size[0]

            for obj in self.objects:
                hitlist.extend(obj.intersection(ray))

            if not hitlist.empty():
                hit = hitlist.nearest_hit()
                hit_color = (255, 255, 255)
                img.putpixel((x, y), hit_color)

        img.save("tracer.png")
