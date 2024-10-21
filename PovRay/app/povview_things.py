#!/usr/bin/env python3

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("GooCanvas", "3.0")
from gi.repository import Gtk, GooCanvas

from math import cos, sin, pi, sqrt

SUBDIV = 100


class ThreeD_object:
    def __init__(self):
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

    def __init__(self, cone_data):
        self.tc = cone_data[0]
        self.tr = cone_data[1]
        self.bc = cone_data[2]
        self.br = cone_data[3]

        self.create_wireframe()

    def __str__(self):
        return (
            f"Cone:\n"
            f"top:    {self.tc[0]:10g}, {self.tc[1]:10g}, {self.tc[2]:10g}"
            f" radius: {self.tr:10g}\n"
            f"bottom: {self.bc[0]:10g}, {self.bc[1]:10g}, {self.bc[2]:10g}"
            f" radius: {self.br:10g}\n"
        )

    def create_wireframe(self):
        self.tx = []
        self.ty = []
        self.tz = []
        self.bx = []
        self.by = []
        self.bz = []
        dsub = 2 * pi / SUBDIV

        for i in range(SUBDIV):
            self.tx += [self.tc[0] + self.tr * cos(dsub * i)]
            self.ty += [-self.tc[1]]
            self.tz += [self.tc[2] + self.tr * sin(dsub * i)]

            self.bx += [self.bc[0] + self.br * cos(dsub * i)]
            self.by += [-self.bc[1]]
            self.bz += [self.bc[2] + self.br * sin(dsub * i)]

    def to_svg(self, view):
        match view:
            case "xy":
                # Top surface (XY-plane)
                svg = f"M{self.tx[0]:g},{self.ty[0]:g} "
                for s in range(1, SUBDIV):
                    svg += f"L{self.tx[s]:g},{self.ty[s]:g} "
                svg += "Z "

                # Bottom surface (XY-plane)
                svg += f"M{self.bx[0]:g},{self.by[0]:g} "
                for s in range(1, SUBDIV):
                    svg += f"L{self.bx[s]:g},{self.by[s]:g} "
                svg += "Z "

                # 'Vertical' spokes connecting top and bottom surfaces
                for s in range(SUBDIV):
                    svg += (
                        f"M{self.tx[s]:g},{self.ty[s]:g} "
                        f"L{self.bx[s]:g},{self.by[s]:g} "
                    )

            case "zy":
                # Top surface (ZY-plane)
                svg = f"M{self.tz[0]:g},{self.ty[0]:g} "
                for s in range(1, SUBDIV):
                    svg += f"L{self.tz[s]:g},{self.ty[s]:g} "
                svg += "Z "

                # Bottom surface (ZY-plane)
                svg += f"M{self.bz[0]:g},{self.by[0]:g} "
                for s in range(1, SUBDIV):
                    svg += f"L{self.bz[s]:g},{self.by[s]:g} "
                svg += "Z "

                # 'Vertical' spokes connecting top and bottom surfaces
                for s in range(SUBDIV):
                    svg += (
                        f"M{self.tz[s]:g},{self.ty[s]:g} "
                        f"L{self.bz[s]:g},{self.by[s]:g} "
                    )

            case "zx":
                # Top surface (ZX-plane)
                svg = f"M{self.tz[0]:g},{self.tx[0]:g} "
                for s in range(1, SUBDIV):
                    svg += f"L{self.tz[s]:g},{self.tx[s]:g} "
                svg += "Z "

                # Bottom surface (ZX-plane)
                svg += f"M{self.bz[0]:g},{self.bx[0]:g} "
                for s in range(1, SUBDIV):
                    svg += f"L{self.bz[s]:g},{self.bx[s]:g} "
                svg += "Z "

                # 'Vertical' spokes connecting top and bottom surfaces
                for s in range(SUBDIV):
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
    def __init__(self, ovus_data):
        self.base_point = (0, 0, 0)
        self.bottom_radius = ovus_data[0]
        self.top_radius = ovus_data[1]

        self.A, self.B, self.C, self.D = self.get_ABCD()

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
        from sympy import symbols, Eq, solve, re, im

        x, y = symbols("x y")

        x1, y1, r1 = ctr1[0], ctr1[1], r1
        x2, y2, r2 = ctr2[0], ctr2[1], r2

        circle1 = Eq((x - x1) ** 2 + (y - y1) ** 2, r1**2)
        circle2 = Eq((x - x2) ** 2 + (y - y2) ** 2, r2**2)

        solutions = solve((circle1, circle2), (x, y))
        if any(
            [im(solution[0]) != 0 or im(solution[1]) != 0 for solution in solutions]
        ):
            solutions = (re(solutions[0][0]), re(solutions[0][1]))

        return solutions

    def get_ABCD(self):
        self.ctr1 = (self.base_point[0], self.base_point[1])
        self.ctr2 = (self.base_point[0], self.base_point[1] + self.bottom_radius)
        join_curve_centers = self.get_intersection(
            ctr1=self.ctr2,
            r1=self.bottom_radius,
            ctr2=self.ctr1,
            r2=self.top_radius,
        )

        # TODO: Maybe check len(join_curve_centers) == 2
        A = self.get_intersection(
            ctr1=join_curve_centers[1],
            r1=self.bottom_radius + self.top_radius,
            ctr2=self.ctr1,
            r2=self.bottom_radius,
        )
        B = self.get_intersection(
            ctr1=join_curve_centers[1],
            r1=self.bottom_radius + self.top_radius,
            ctr2=self.ctr2,
            r2=self.top_radius,
        )
        C = self.get_intersection(
            ctr1=join_curve_centers[0],
            r1=self.bottom_radius + self.top_radius,
            ctr2=self.ctr2,
            r2=self.top_radius,
        )
        D = self.get_intersection(
            ctr1=join_curve_centers[0],
            r1=self.bottom_radius + self.top_radius,
            ctr2=self.ctr1,
            r2=self.bottom_radius,
        )

        return A, B, C, D

    def get_radius(self, initial_radius: float, relative_height: float):
        return sqrt(initial_radius**2 - relative_height**2)

    def lerp(self, alpha, A, B):
        return A + (B - A) * alpha

    def create_wireframe(self):
        self.tx = []
        self.ty = []
        self.tz = []
        self.bx = []
        self.by = []
        self.bz = []
        dsub = 2 * pi / SUBDIV

        for i in range(SUBDIV):
            self.tx += [
                self.base_point[0]
                + self.get_radius(self.top_radius, self.B[1] - self.ctr2[1])
                * cos(dsub * i)
            ]
            self.ty += [-self.B[1]]
            self.tz += [
                self.base_point[2]
                + self.get_radius(self.top_radius, self.B[1] - self.ctr2[1])
                * sin(dsub * i)
            ]

            self.bx += [
                self.base_point[0]
                + self.get_radius(self.bottom_radius, self.A[1] - self.ctr1[1])
                * cos(dsub * i)
            ]
            self.by += [-self.A[1]]
            self.bz += [
                self.base_point[2]
                + self.get_radius(self.bottom_radius, self.A[1] - self.ctr1[1])
                * sin(dsub * i)
            ]

        self.bpx = self.base_point[0]
        self.bpy = -(self.base_point[1] - self.bottom_radius)
        self.bpz = self.base_point[2]
        self.tpx = self.base_point[0]
        self.tpy = -(self.base_point[1] + self.bottom_radius + self.top_radius)
        self.tpz = self.base_point[2]

    def to_svg(self, view):
        match view:
            case "xy":
                # Top circle (XY-plane)
                svg = f"M{self.tx[0]:g},{self.ty[0]:g} "
                for s in range(1, SUBDIV):
                    svg += f"L{self.tx[s]:g},{self.ty[s]:g} "
                svg += "Z "

                # Bottom circle (XY-plane)
                svg += f"M{self.bx[0]:g},{self.by[0]:g} "
                for s in range(1, SUBDIV):
                    svg += f"L{self.bx[s]:g},{self.by[s]:g} "
                svg += "Z "

                # Meridian lines
                for s in range(SUBDIV):
                    svg += f"M{self.bpx:g},{self.bpy:g} "
                    if self.tx[s] > self.base_point[0]:
                        svg += (
                            f"A{self.bottom_radius:g},{self.bottom_radius:g} 0 0,0 {self.bx[s]:g},{self.by[s]:g} "
                            f"A{self.top_radius+self.bottom_radius:g},{self.top_radius+self.bottom_radius:g} 0 0,0 {self.tx[s]:g},{self.ty[s]:g} "
                            f"A{self.top_radius:g},{self.top_radius:g} 0 0,0 {self.tpx:g},{self.tpy:g} "
                        )
                    elif self.tx[s] < self.base_point[0]:
                        svg += (
                            f"A{self.bottom_radius:g},{self.bottom_radius:g} 0 0,1 {self.bx[s]:g},{self.by[s]:g} "
                            f"A{self.top_radius+self.bottom_radius:g},{self.top_radius+self.bottom_radius:g} 0 0,1 {self.tx[s]:g},{self.ty[s]:g} "
                            f"A{self.top_radius:g},{self.top_radius:g} 0 0,1 {self.tpx:g},{self.tpy:g} "
                        )
                    else:
                        svg += (
                            f"L{self.bx[s]:g},{self.by[s]:g} "
                            f"L{self.tx[s]:g},{self.ty[s]:g} "
                            f"L{self.tpx:g},{self.tpy:g} "
                        )

            case "zy":
                # Top circle (ZY-plane)
                svg = f"M{self.tz[0]:g},{self.ty[0]:g} "
                for s in range(1, SUBDIV):
                    svg += f"L{self.tz[s]:g},{self.ty[s]:g} "
                svg += "Z "

                # Bottom circle (ZY-plane)
                svg += f"M{self.bz[0]:g},{self.by[0]:g} "
                for s in range(1, SUBDIV):
                    svg += f"L{self.bz[s]:g},{self.by[s]:g} "
                svg += "Z "

                # Meridian lines
                for s in range(SUBDIV):
                    svg += f"M{self.bpz:g},{self.bpy:g} "

                    if self.tz[s] > self.base_point[2]:
                        svg += (
                            f"A{self.bottom_radius:g},{self.bottom_radius:g} 0 0,0 {self.bz[s]:g},{self.by[s]:g} "
                            f"A{self.top_radius+self.bottom_radius:g},{self.top_radius+self.bottom_radius:g} 0 0,0 {self.tz[s]:g},{self.ty[s]:g} "
                            f"A{self.top_radius:g},{self.top_radius:g} 0 0,0 {self.tpz:g},{self.tpy:g} "
                        )
                    elif self.tz[s] < self.base_point[2]:
                        svg += (
                            f"A{self.bottom_radius:g},{self.bottom_radius:g} 0 0,1 {self.bz[s]:g},{self.by[s]:g} "
                            f"A{self.top_radius+self.bottom_radius:g},{self.top_radius+self.bottom_radius:g} 0 0,1 {self.tz[s]:g},{self.ty[s]:g} "
                            f"A{self.top_radius:g},{self.top_radius:g} 0 0,1 {self.tpz:g},{self.tpy:g} "
                        )
                    else:
                        svg += (
                            f"L{self.bz[s]:g},{self.by[s]:g} "
                            f"L{self.tz[s]:g},{self.ty[s]:g} "
                            f"L{self.tpz:g},{self.tpy:g} "
                        )

            case "zx":
                # Top circle (ZX-plane)
                svg = f"M{self.tz[0]:g},{self.tx[0]:g} "
                for s in range(1, SUBDIV):
                    svg += f"L{self.tz[s]:g},{self.tx[s]:g} "
                svg += "Z "

                # Bottom circle (ZX-plane)
                svg += f"M{self.bz[0]:g},{self.bx[0]:g} "
                for s in range(1, SUBDIV):
                    svg += f"L{self.bz[s]:g},{self.bx[s]:g} "
                svg += "Z "

                # Meridian lines
                for s in range(SUBDIV):
                    svg += (
                        f"M{self.bpz:g},{self.bpx:g} "
                        f"L{self.bz[s]:g},{self.bx[s]:g} "
                        f"L{self.tz[s]:g},{self.tx[s]:g} "
                        f"L{self.tpz:g},{self.tpx:g} "
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
