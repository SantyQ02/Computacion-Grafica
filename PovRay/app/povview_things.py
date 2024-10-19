#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  povview_things.py
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


import gi

gi.require_version("Gtk", "3.0")
gi.require_version("GooCanvas", "3.0")
from gi.repository import Gtk, GooCanvas

from math import cos, sin, pi

SUBDIV = 12


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

        print(self.tx)
        print(self.ty)
        print(self.tz)
        print(self.bx)
        print(self.by)
        print(self.bz)

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
        self.bottom_radius = ovus_data[0]
        self.top_radius = ovus_data[1]

    def __str__(self):
        return (
            f"Ovus:\n"
            f"bottom radius: {self.bottom_radius:10g}\n"
            f"top radius:    {self.top_radius:10g}\n"
        )

    def create_wireframe(self):
        pass

    def to_svg(self, view):
        match view:
            case "xy":
                pass
            case "zy":
                pass
            case "zx":
                pass
            case _:
                raise ValueError("Invalid view")

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