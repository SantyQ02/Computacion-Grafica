#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  povview_minitracer.py
#
#  Copyright 2024 John Coppens <john@jcoppens.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#


import pylab as plt
import numpy as np

from povview_parser import make_parser
from povview_math import Vec3, Ray, Hit, Hit_list
from math import tan, radians, sqrt

from PIL import Image

from pdb import set_trace as st

SCENE = """
sphere { 
    <0, 0, 0>, 5
}
"""


def intersection(ray: Ray, obj):
    """Rutina de cálculo de los eventuales puntos de intersección entre un rayo
    y un objeto (en este caso una esfera). Normalmente, la definición de
    la rutina de intersección debería formar parte de la clases de
    cada tipo de objeto.
    """
    loc = Vec3(obj[1])
    rad = obj[2]

    # Ver cg_math.pdf para explicación del cálculo
    a = 1  #  R1 • R1 = 1
    b = ray.direction * (ray.location - loc) * 2  #  2(R1 • (R0 − C)
    c = abs(ray.location - loc) ** 2 - rad**2  #  ||R0 − C||^2 − r^2

    if b**2 < 4 * c:
        return []

    elif b**2 == 4 * c:
        return [Hit(obj, -b / 2)]

    else:
        return [
            Hit(obj, (-b - sqrt(b**2 - 4 * c)) / 2),
            Hit(obj, (-b + sqrt(b**2 - 4 * c)) / 2),
        ]


def ray_generator(w, h, loc, angle):
    """Generador de rayos. En el caso de umplementar el tracer con múltiples
    hilos o procesadores, esta rutina distribuye la tarea entre los
    rasterizadores. Eso se puede hacer, ya que no hay interacción entre
    cada rayo.

    El generador de rayos 'entrega' a cada cliente:
        - la ubicación de la 'cámara'
        - la dirección del rayo
        - el número del pixel (para poder calcular x, y)
    """
    width = abs(loc.z) * 2 * tan(radians(angle) / 2)  # Ancho físico de la 'pantalla'
    pixel = width / w  # Ancho de 1 pixel

    for i in range(w * h):
        x = (i % w) - (w // 2) + 0.5
        y = (i // w) - (h // 2) + 0.5
        x *= pixel
        y *= pixel
        direction = Vec3(x - loc.x, y - loc.y, 0 - loc.z)

        yield Ray(loc, direction.normalized()), i


def graph_trace(scene):
    """Tracing gráfico, utilizando una image creada por la librería PIL.
    Aunque estaremos escribiendo pixel por pixel en modo RGB, en este
    demo el color será siempre Amarillo, y la intensidad es máxima
    """
    size = 640, 360  # Tamaño de la imagen generada (w, h)
    img = Image.new("RGB", size, 0)
    parser = make_parser()
    parsed = parser.parse_string(scene)
    raygen = ray_generator(*size, Vec3(0, 0, -40), 30)

    for ray, i in raygen:
        for obj in parsed.as_list():
            img.putpixel(
                (i % size[0], i // size[0]),
                (255, 255, 0) if intersection(ray, obj) else (0, 0, 0),
            )

    img.show()


def main(args):
    # plot_rays()
    # trace(SCENE)
    graph_trace(SCENE)
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))

"""
Otras formas de Tracer
"""

# def plot_rays():
#     """ Grafica los puntos finales de un vector unitario, que itera sobre
#         todas las direcciones que calcula el generador de rayos. La intención
#         es mostrar que es importante la distorción de la perspectiva por
#         la cercanía a la pantalla.
#     """
#     raygen = ray_generator(32, 18, Vec3(0, 0, -4), 60)
#     mpl_plot_rays(raygen)
#     return 0

# def mpl_plot_rays(raygen):
#     x = []; y = []
#     for r, i in raygen:
#         d = r.direction
#         x.append(d.x)
#         y.append(d.y)

#     plt.plot(x, y, '.')
#     plt.title('Gráfico de los puntos finales de los rayos')
#     plt.axis('equal')
#     plt.show()


# def trace(scene):
#     """ Tracing en modo 'text'. El tracer imprime una letra 'M' en caso de
#         intersección, y un espacio si no hay intersección.
#     """
#     parser = make_pov_parser()
#     parsed = parser.parse_string(scene)
#     # ~ print(parsed.dump())
#     raygen = ray_generator(32, 18, Vec3(0, 0, -4), 40)

#     for ray, i in raygen:
#         for obj in parsed.as_list():
#             if intersection(ray, obj):
#                 print('X', end = '')
#             else:
#                 print(' ', end = '')
#             if i % 32 == 0: print()
