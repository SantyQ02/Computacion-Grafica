#!/usr/bin/env python3

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("GooCanvas", "3.0")
from gi.repository import Gtk, GooCanvas
from sympy import symbols, Eq, solve, re, im, N
import numpy as np

from math import cos, sin, pi, sqrt, radians


class ThreeD_object:
    def __init__(
        self,
        CIRCULAR_SUBDIV=100,
        VERTICAL_SUBDIV=100,
        ROTATION_VECTOR=[0, 0, 0],
        SQUARED=False,
    ):
        self._CIRCULAR_SUBDIV = CIRCULAR_SUBDIV
        self._VERTICAL_SUBDIV = VERTICAL_SUBDIV
        self._ROTATION_VECTOR = ROTATION_VECTOR
        self._SQUARED = SQUARED

    def set_CIRCULAR_SUBDIV(self, CIRCULAR_SUBDIV):
        self._CIRCULAR_SUBDIV = CIRCULAR_SUBDIV

    def set_VERTICAL_SUBDIV(self, VERTICAL_SUBDIV):
        self._VERTICAL_SUBDIV = VERTICAL_SUBDIV

    def set_ROTATION_VECTOR(self, ROTATION_VECTOR):
        self._ROTATION_VECTOR = ROTATION_VECTOR

    def set_SQUARED(self, SQUARED):
        self._SQUARED = SQUARED

    def set_params(self, CIRCULAR_SUBDIV, VERTICAL_SUBDIV, ROTATION_VECTOR, SQUARED):
        self.set_CIRCULAR_SUBDIV(CIRCULAR_SUBDIV)
        self.set_VERTICAL_SUBDIV(VERTICAL_SUBDIV)
        self.set_ROTATION_VECTOR(ROTATION_VECTOR)
        self.set_SQUARED(SQUARED)
        self.create_wireframe()

    def create_wireframe(self):
        pass


class Vec3:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z


class RGB:
    def __init__(self, r, g=None, b=None):
        if isinstance(r, list):
            self._rgb = r
        else:
            self._rgb = [r, g, b]

    def __str__(self):
        return f"r: {self._rgb[0]}, g: {self._rgb[1]}, b: {self._rgb[2]}"

    @property
    def r(self):
        return self._rgb[0]

    @property
    def g(self):
        return self._rgb[1]

    @property
    def b(self):
        return self._rgb[2]

    @property
    def rgb(self):
        return self._rgb


class RGBA:
    def __init__(self, r, g, b, a):
        self.r, self.g, self.b, self.a = r, g, b, a


class Cone(ThreeD_object):
    """
    tc      self.tc     vec3    Cone top center
    tr      self.tr     float   Cone top radius
    bc      self.bc     vec3    Cone bottom center
    br      self.br     float   Cone bottom radius
    """

    # TODO: Update interface to parsed values
    def __init__(self, cone_data, **kwargs):
        super().__init__(**kwargs)
        self.tc = cone_data[0]
        self.tr = cone_data[1]
        self.bc = cone_data[2]
        self.br = cone_data[3]

        self.create_ovus_wireframe()

    def __str__(self):
        return (
            f"Cone:\n"
            f"top:    {self.tc[0]:10g}, {self.tc[1]:10g}, {self.tc[2]:10g}"
            f" radius: {self.tr:10g}\n"
            f"bottom: {self.bc[0]:10g}, {self.bc[1]:10g}, {self.bc[2]:10g}"
            f" radius: {self.br:10g}\n"
        )

    def create_ovus_wireframe(self):
        self.tx = []
        self.ty = []
        self.tz = []
        self.bx = []
        self.by = []
        self.bz = []
        circ_sub = 2 * pi / self._self._CIRCULAR_SUBDIV

        for i in range(self._self._CIRCULAR_SUBDIV):
            self.tx += [self.tc[0] + self.tr * cos(circ_sub * i)]
            self.ty += [-self.tc[1]]
            self.tz += [self.tc[2] + self.tr * sin(circ_sub * i)]

            self.bx += [self.bc[0] + self.br * cos(circ_sub * i)]
            self.by += [-self.bc[1]]
            self.bz += [self.bc[2] + self.br * sin(circ_sub * i)]

    def to_svg(self, view):
        match view:
            case "xy":
                # Top surface (XY-plane)
                svg = f"M{self.tx[0]:g},{self.ty[0]:g} "
                for s in range(1, self._self._CIRCULAR_SUBDIV):
                    svg += f"L{self.tx[s]:g},{self.ty[s]:g} "
                svg += "Z "

                # Bottom surface (XY-plane)
                svg += f"M{self.bx[0]:g},{self.by[0]:g} "
                for s in range(1, self._self._CIRCULAR_SUBDIV):
                    svg += f"L{self.bx[s]:g},{self.by[s]:g} "
                svg += "Z "

                # 'Vertical' spokes connecting top and bottom surfaces
                for s in range(self._self._CIRCULAR_SUBDIV):
                    svg += (
                        f"M{self.tx[s]:g},{self.ty[s]:g} "
                        f"L{self.bx[s]:g},{self.by[s]:g} "
                    )

            case "zy":
                # Top surface (ZY-plane)
                svg = f"M{self.tz[0]:g},{self.ty[0]:g} "
                for s in range(1, self._CIRCULAR_SUBDIV):
                    svg += f"L{self.tz[s]:g},{self.ty[s]:g} "
                svg += "Z "

                # Bottom surface (ZY-plane)
                svg += f"M{self.bz[0]:g},{self.by[0]:g} "
                for s in range(1, self._CIRCULAR_SUBDIV):
                    svg += f"L{self.bz[s]:g},{self.by[s]:g} "
                svg += "Z "

                # 'Vertical' spokes connecting top and bottom surfaces
                for s in range(self._CIRCULAR_SUBDIV):
                    svg += (
                        f"M{self.tz[s]:g},{self.ty[s]:g} "
                        f"L{self.bz[s]:g},{self.by[s]:g} "
                    )

            case "zx":
                # Top surface (ZX-plane)
                svg = f"M{self.tz[0]:g},{self.tx[0]:g} "
                for s in range(1, self._CIRCULAR_SUBDIV):
                    svg += f"L{self.tz[s]:g},{self.tx[s]:g} "
                svg += "Z "

                # Bottom surface (ZX-plane)
                svg += f"M{self.bz[0]:g},{self.bx[0]:g} "
                for s in range(1, self._CIRCULAR_SUBDIV):
                    svg += f"L{self.bz[s]:g},{self.bx[s]:g} "
                svg += "Z "

                # 'Vertical' spokes connecting top and bottom surfaces
                for s in range(self._CIRCULAR_SUBDIV):
                    svg += (
                        f"M{self.tz[s]:g},{self.tx[s]:g} "
                        f"L{self.bz[s]:g},{self.bx[s]:g} "
                    )

            case _:
                raise ValueError("Invalid view")

        return svg.strip()

    def draw_on(self, views):
        for view in ["xy", "zy", "zx"]:
            root = views[view]["canvas"].get_root_item()
            GooCanvas.CanvasPath(
                parent=root,
                data=self.to_svg(view),
                line_width=1,
                stroke_color="Black",
                fill_color=None,
            )


class Ovus(ThreeD_object):
    def __init__(self, ovus_data, **kwargs):
        super().__init__(**kwargs)
        self.base_point = (0, 0, 0)
        self.bottom_radius = ovus_data["bottom_radius"]
        self.top_radius = ovus_data["top_radius"]
        self.color = ovus_data["color"]

        self.is_sphere = not 0 < self.top_radius < 2 * self.bottom_radius

        if not self.is_sphere:
            self.bottom_interval, self.top_interval = self.get_intervals()

        self.create_wireframe()

    def __str__(self):
        return (
            f"Ovus:\n"
            f"bottom radius: {self.bottom_radius:10g}\n"
            f"top radius:    {self.top_radius:10g}\n"
        )

    def get_intersection(
        self, *, ctr1: tuple[float], r1: float, ctr2: tuple[float], r2: float
    ):
        x, y = symbols("x y")

        x1, y1, r1 = ctr1[0], ctr1[1], r1
        x2, y2, r2 = ctr2[0], ctr2[1], r2

        circle1 = Eq((x - x1) ** 2 + (y - y1) ** 2, r1**2)
        circle2 = Eq((x - x2) ** 2 + (y - y2) ** 2, r2**2)

        solutions = solve((circle1, circle2), (x, y))
        if any(
            [im(solution[0]) != 0 or im(solution[1]) != 0 for solution in solutions]
        ):
            solutions = [(re(solutions[0][0]), re(solutions[0][1]))]

        solutions = [
            (float(N(solution[0])), float(N(solution[1]))) for solution in solutions
        ]

        return solutions

    def get_intervals(self):
        self.bottom_center = (self.base_point[0], self.base_point[1])
        self.top_center = (self.base_point[0], self.base_point[1] + self.bottom_radius)
        self.join_curve_centers = self.get_intersection(
            ctr1=self.top_center,
            r1=self.bottom_radius,
            ctr2=self.bottom_center,
            r2=self.top_radius,
        )

        A = self.get_intersection(
            ctr1=self.join_curve_centers[1],
            r1=self.bottom_radius + self.top_radius,
            ctr2=self.bottom_center,
            r2=self.bottom_radius,
        )[0]
        B = self.get_intersection(
            ctr1=self.join_curve_centers[1],
            r1=self.bottom_radius + self.top_radius,
            ctr2=self.top_center,
            r2=self.top_radius,
        )[0]

        return A[1], B[1]

    def get_radius(self, initial_radius: float, relative_height: float):
        return sqrt(initial_radius**2 - relative_height**2)

    def get_ovus_radius(self, y: float):
        if y < self.bottom_interval:
            return self.get_radius(self.bottom_radius, y - self.bottom_center[1])
        elif y < self.top_interval:
            return self.get_radius(
                self.bottom_radius + self.top_radius, y - self.join_curve_centers[1][1]
            ) - (self.join_curve_centers[1][0] - self.base_point[0])
        else:
            return self.get_radius(self.top_radius, y - self.top_center[1])

    def create_wireframe(self):
        if self.is_sphere:
            self.create_sphere_wireframe()
        else:
            self.create_ovus_wireframe()

    def create_ovus_wireframe(self):
        circ_sub = 2 * pi / self._CIRCULAR_SUBDIV

        self.bottom_point = [
            self.base_point[0],
            self.base_point[1] - self.bottom_radius,
            self.base_point[2],
        ]
        self.top_point = [
            self.base_point[0],
            self.base_point[1] + self.bottom_radius + self.top_radius,
            self.base_point[2],
        ]

        self.vertical_floors = []
        max_radius = 0
        for i in range(1, self._VERTICAL_SUBDIV):
            y = (
                abs(self.top_point[1] - self.bottom_point[1]) / self._VERTICAL_SUBDIV
            ) * i + self.bottom_point[1]
            radius = self.get_ovus_radius(y)
            if radius > max_radius:
                max_radius = radius
                self.max_radius_floor = i - 1

            self.vertical_floors.append(
                [
                    self.apply_rotation(
                        self._ROTATION_VECTOR,
                        [
                            self.base_point[0] + radius * cos(circ_sub * j),
                            -y,
                            self.base_point[2] + radius * sin(circ_sub * j),
                        ],
                    )
                    for j in range(self._CIRCULAR_SUBDIV)
                ]
            )

        self.bottom_point[1], self.top_point[1] = (
            -self.bottom_point[1],
            -self.top_point[1],
        )

        self.bottom_point, self.top_point = self.apply_rotation(
            self._ROTATION_VECTOR, self.bottom_point
        ), self.apply_rotation(self._ROTATION_VECTOR, self.top_point)

    def create_sphere_wireframe(self):
        circ_sub = 2 * pi / self._CIRCULAR_SUBDIV

        sphere_radius = max(self.bottom_radius, self.top_radius)

        self.bottom_point = [
            self.base_point[0],
            self.base_point[1] - sphere_radius,
            self.base_point[2],
        ]
        self.top_point = [
            self.base_point[0],
            self.base_point[1] + sphere_radius,
            self.base_point[2],
        ]

        self.vertical_floors = []
        max_radius = 0
        for i in range(1, self._VERTICAL_SUBDIV):
            y = (
                abs(self.top_point[1] - self.bottom_point[1]) / self._VERTICAL_SUBDIV
            ) * i + self.bottom_point[1]
            radius = self.get_radius(sphere_radius, y - self.base_point[1])
            if radius > max_radius:
                max_radius = radius
                self.max_radius_floor = i - 1

            self.vertical_floors.append(
                [
                    self.apply_rotation(
                        self._ROTATION_VECTOR,
                        [
                            self.base_point[0] + radius * cos(circ_sub * j),
                            -y,
                            self.base_point[2] + radius * sin(circ_sub * j),
                        ],
                    )
                    for j in range(self._CIRCULAR_SUBDIV)
                ]
            )

        self.bottom_point[1], self.top_point[1] = (
            -self.bottom_point[1],
            -self.top_point[1],
        )

        self.bottom_point, self.top_point = self.apply_rotation(
            self._ROTATION_VECTOR, self.bottom_point
        ), self.apply_rotation(self._ROTATION_VECTOR, self.top_point)

    def apply_rotation(self, angle_vector: list[float], vector: list[float]):
        angle_vector = [radians(angle) for angle in angle_vector]
        x_rotation_matrix = np.array(
            [
                [1, 0, 0],
                [0, cos(angle_vector[0]), -sin(angle_vector[0])],
                [0, sin(angle_vector[0]), cos(angle_vector[0])],
            ]
        )
        y_rotation_matrix = np.array(
            [
                [cos(angle_vector[1]), 0, sin(angle_vector[1])],
                [0, 1, 0],
                [-sin(angle_vector[1]), 0, cos(angle_vector[1])],
            ]
        )
        z_rotation_matrix = np.array(
            [
                [cos(angle_vector[2]), -sin(angle_vector[2]), 0],
                [sin(angle_vector[2]), cos(angle_vector[2]), 0],
                [0, 0, 1],
            ]
        )
        rotation_matrix = np.matmul(
            np.matmul(x_rotation_matrix, y_rotation_matrix), z_rotation_matrix
        )

        vector = np.array(vector)
        return np.matmul(rotation_matrix, vector)

    def to_svg(self, view):
        svg = ""
        match view:
            case "xy":
                # Max radius
                svg += f"M{self.vertical_floors[self.max_radius_floor][0][0]:g},{self.vertical_floors[self.max_radius_floor][0][1]:g} Z"
                for j in range(1, self._CIRCULAR_SUBDIV):
                    svg += f"L{self.vertical_floors[self.max_radius_floor][j][0]:g},{self.vertical_floors[self.max_radius_floor][j][1]:g} "
                svg += "Z "

                # Meridian lines
                for j in range(self._CIRCULAR_SUBDIV):
                    svg += f"M{self.bottom_point[0]:g},{self.bottom_point[1]:g} "
                    for s in range(self._VERTICAL_SUBDIV - 1):
                        svg += f"L{self.vertical_floors[s][j][0]:g},{self.vertical_floors[s][j][1]:g} "
                    svg += f"L{self.top_point[0]:g},{self.top_point[1]:g} "

                # Ecuator lines
                if self._SQUARED:
                    for s in range(self._VERTICAL_SUBDIV - 1):
                        svg += f"M{self.vertical_floors[s][0][0]:g},{self.vertical_floors[s][0][1]:g} "
                        for j in range(1, self._CIRCULAR_SUBDIV):
                            svg += f"L{self.vertical_floors[s][j][0]:g},{self.vertical_floors[s][j][1]:g} "
                        svg += "Z"

            case "zy":
                # Max radius
                svg += f"M{self.vertical_floors[self.max_radius_floor][0][2]:g},{self.vertical_floors[self.max_radius_floor][0][1]:g} Z"
                for j in range(1, self._CIRCULAR_SUBDIV):
                    svg += f"L{self.vertical_floors[self.max_radius_floor][j][2]:g},{self.vertical_floors[self.max_radius_floor][j][1]:g} "
                svg += "Z "

                # Meridian lines
                for j in range(self._CIRCULAR_SUBDIV):
                    svg += f"M{self.bottom_point[2]:g},{self.bottom_point[1]:g} "
                    for s in range(self._VERTICAL_SUBDIV - 1):
                        svg += f"L{self.vertical_floors[s][j][2]:g},{self.vertical_floors[s][j][1]:g} "
                    svg += f"L{self.top_point[2]:g},{self.top_point[1]:g} "

                # Ecuator lines
                if self._SQUARED:
                    for s in range(self._VERTICAL_SUBDIV - 1):
                        svg += f"M{self.vertical_floors[s][0][2]:g},{self.vertical_floors[s][0][1]:g} "
                        for j in range(1, self._CIRCULAR_SUBDIV):
                            svg += f"L{self.vertical_floors[s][j][2]:g},{self.vertical_floors[s][j][1]:g} "
                        svg += "Z"

            case "zx":
                # Max radius
                svg += f"M{self.vertical_floors[self.max_radius_floor][0][2]:g},{self.vertical_floors[self.max_radius_floor][0][0]:g} Z"
                for j in range(1, self._CIRCULAR_SUBDIV):
                    svg += f"L{self.vertical_floors[self.max_radius_floor][j][2]:g},{self.vertical_floors[self.max_radius_floor][j][0]:g} "
                svg += "Z "

                # Meridian lines
                for j in range(self._CIRCULAR_SUBDIV):
                    svg += f"M{self.bottom_point[2]:g},{self.bottom_point[0]:g} "
                    for s in range(self._VERTICAL_SUBDIV - 1):
                        svg += f"L{self.vertical_floors[s][j][2]:g},{self.vertical_floors[s][j][0]:g} "
                    svg += f"L{self.top_point[2]:g},{self.top_point[0]:g} "

                # Ecuator lines
                if self._SQUARED:
                    for s in range(self._VERTICAL_SUBDIV - 1):
                        svg += f"M{self.vertical_floors[s][0][2]:g},{self.vertical_floors[s][0][0]:g} "
                        for j in range(1, self._CIRCULAR_SUBDIV):
                            svg += f"L{self.vertical_floors[s][j][2]:g},{self.vertical_floors[s][j][0]:g} "
                        svg += "Z"

            case _:
                raise ValueError("Invalid view")

        return svg.strip()

    def draw_on(self, views):
        for view in ["xy", "zy", "zx"]:
            root = views[view]["canvas"].get_root_item()
            GooCanvas.CanvasPath(
                parent=root,
                data=self.to_svg(view),
                line_width=1,
                stroke_color="Black",
                fill_color=None,
            )


# %%
