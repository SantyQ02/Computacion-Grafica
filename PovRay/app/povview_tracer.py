import pylab as plt
import numpy as np

from povview_parser import make_pov_parser, make_catalog
from povview_math import Vec3, RGB, Ray, Hit, HitList
from math import tan, radians, sqrt

from PIL import Image


def ray_generator(w, h, loc, angle):
    """
    Generador de rayos. En el caso de implementar el tracer con múltiples
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

        yield Ray(loc, direction.normalized())


def mpl_plot_rays(raygen):
    x = []
    y = []
    for r in raygen:
        d = r.direction
        x.append(d.x)
        y.append(d.y)

    plt.plot(x, y, ".")
    plt.title("Gráfico de los puntos finales de los rayos")
    plt.axis("equal")
    plt.show()


AMBIENT = 0.2


def tracer(size, scene_catalog):
    """
    Tracing gráfico, utilizando una image creada por la librería PIL.
    Aunque estaremos escribiendo pixel por pixel en modo RGB, en este
    demo el color será siempre Amarillo, y la intensidad es máxima
    """
    img = Image.new("RGB", size, 0)
    cameras = scene_catalog["cameras"]
    things = scene_catalog["things"]
    lights = scene_catalog["lights"]

    raygen = ray_generator(*size, Vec3(0, 0, -40), 30)
    hitlist = HitList()

    for ray, i in raygen:
        hitlist.clear()  # Cada rayo borramos la list de hits
        x, y = i % size[0], i // size[0]

        # Para cada objeto:
        for thing in things:

            # Nos fijamos si está en el camino del rayo y agregamos los impactos
            hitlist.append(thing.intersection(ray))

        # ~ # Si hay alguna intersection
        # ~ if not hitlist.empty():
        # ~ for light in lights:
        # ~ light_ray = Ray(hit_loc, (light_loc - hit_loc).normalized())

        # ~ for obj in things:
        # ~ hits = thingie.intersection(light_ray)
        # ~ for hit in hits:
        # ~ if hit.t > EPSILON:
        # ~ fact = 0        # (1 - AMBIENT)
        # ~ break

        # ~ if fact == 0:
        # ~ break

        # ~ cos1 = (AMBIENT +
        # ~ normal * (light_loc - ray.at(t)).normalized() * fact)
        # ~ hit_color = hit_color + thing_rgb.reflect(light_rgb) * cos1
        # ~ img.putpixel((x, y), hit_color.as_rgb8())
        
    img.show()


def main(args):
    parser = make_pov_parser()
    parsed = parser.parse_string(SCENE)
    catalog = make_catalog(parsed)
    print(parsed, catalog)
    tracer((400, 320), catalog)
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))
