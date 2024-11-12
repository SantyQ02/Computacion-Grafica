#!/usr/bin/env python3

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("GooCanvas", "3.0")
from gi.repository import GooCanvas
from sympy import symbols, Eq, solve, re, im, N
import numpy as np

from math import cos, sin, pi, sqrt, radians

LINE_COLOR = "darkgrey"


class ThreeD_object:
    def __init__(
        self,
        SUBDIV=50,
    ):
        self._SUBDIV = SUBDIV
        self.vertexes = []
        self.edges = []

    def set_SUBDIV(self, SUBDIV):
        self._SUBDIV = SUBDIV

    def set_params(self, SUBDIV):
        self.set_SUBDIV(SUBDIV)

        self.vertexes.clear()
        self.edges.clear()

        self.create_wireframe()

    def create_wireframe(self):
        return

    def apply_rotation(self, angle_vector: list[float]):
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

        for i, vertex in enumerate(self.vertexes):
            self.vertexes[i] = np.matmul(rotation_matrix, np.array(vertex))

    def apply_translation(self, translation_vector: list[float]):
        translation_matrix = np.array(
            [
                [1, 0, 0, translation_vector[0]],
                [0, 1, 0, translation_vector[1]],
                [0, 0, 1, translation_vector[2]],
                [0, 0, 0, 1],
            ]
        )

        for i, vertex in enumerate(self.vertexes):
            self.vertexes[i] = np.delete(
                np.matmul(translation_matrix, np.array(vertex)), -1
            )

    def apply_scale(self, scale_vector: list[float]):
        scale_matrix = np.array(
            [
                [scale_vector[0], 0, 0],
                [0, scale_vector[1], 0],
                [0, 0, scale_vector[2]],
            ]
        )

        for i, vertex in enumerate(self.vertexes):
            self.vertexes[i] = np.matmul(scale_matrix, np.array(vertex))

    def apply_modifiers(self):
        for modifier in self.modifiers:
            match modifier["type"]:
                case "translate":
                    self.apply_translation(modifier["vector"])
                case "rotate":
                    self.apply_rotation(modifier["vector"])
                case "scale":
                    self.apply_scale(modifier["vector"])

    def to_svg(self, view):
        svg = ""
        match view:
            case "xy":
                for edge in self.edges:
                    svg += f"M{self.vertexes[edge[0]][0]:g},{self.vertexes[edge[0]][1]:g} L{self.vertexes[edge[1]][0]:g},{self.vertexes[edge[1]][1]:g} "

            case "zy":
                for edge in self.edges:
                    svg += f"M{self.vertexes[edge[0]][2]:g},{self.vertexes[edge[0]][1]:g} L{self.vertexes[edge[1]][2]:g},{self.vertexes[edge[1]][1]:g} "

            case "zx":
                for edge in self.edges:
                    svg += f"M{self.vertexes[edge[0]][2]:g},{self.vertexes[edge[0]][0]:g} L{self.vertexes[edge[1]][2]:g},{self.vertexes[edge[1]][0]:g} "

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
                stroke_color=LINE_COLOR,
                fill_color=None,
            )


class Cone(ThreeD_object):
    """
    tc      self.top_center     vec3    Cone top center
    tr      self.top_radius     float   Cone top radius
    bc      self.bottom_center     vec3    Cone bottom center
    br      self.bottom_radius     float   Cone bottom radius
    """

    # TODO: Update interface to parsed values
    def __init__(self, cone_data, **kwargs):
        super().__init__(**kwargs)
        self.top_center = cone_data[0]
        self.top_radius = cone_data[1]
        self.bottom_center = cone_data[2]
        self.bottom_radius = cone_data[3]

        self.create_wireframe()

    def __str__(self):
        return (
            f"Cone:\n"
            f"top:    {self.top_center[0]:10g}, {self.top_center[1]:10g}, {self.top_center[2]:10g}"
            f" radius: {self.top_radius:10g}\n"
            f"bottom: {self.bottom_center[0]:10g}, {self.bottom_center[1]:10g}, {self.bottom_center[2]:10g}"
            f" radius: {self.bottom_radius:10g}\n"
        )

    def create_wireframe(self):
        # Vertexes
        circ_sub = 2 * pi / self._SUBDIV

        for i in range(self._SUBDIV):
            self.vertexes.append(
                [
                    self.top_center[0] + self.top_radius * cos(circ_sub * i),
                    -self.top_center[1],
                    self.top_center[2] + self.top_radius * sin(circ_sub * i),
                ]
            )
            self.vertexes.append(
                [
                    self.bottom_center[0] + self.bottom_radius * cos(circ_sub * i),
                    -self.bottom_center[1],
                    self.bottom_center[2] + self.bottom_radius * sin(circ_sub * i),
                ]
            )

        # Edges
        for i in range(self._SUBDIV):
            self.edges.append((i * 2, i * 2 + 1))

        for i in range(self._SUBDIV - 1):
            self.edges.append((i * 2, i * 2 + 2))
            self.edges.append((i * 2 + 1, i * 2 + 3))
        self.edges.append((-1, 1))
        self.edges.append((-2, 0))


class Ovus(ThreeD_object):
    def __init__(self, ovus_data, **kwargs):
        super().__init__(**kwargs)
        self.base_point = (0, 0, 0)
        self.bottom_radius = ovus_data["bottom_radius"]
        self.top_radius = ovus_data["top_radius"]

        self.is_sphere = not 0 < self.top_radius < 2 * self.bottom_radius

        if not self.is_sphere:
            self.bottom_interval, self.top_interval = self.get_intervals()

        self.create_wireframe()

    def __str__(self):
        return (
            f"Ovus:\n"
            f"  bottom radius: {self.bottom_radius:10g}\n"
            f"  top radius:    {self.top_radius:10g}\n"
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
        # Vertexes
        circ_sub = 2 * pi / self._SUBDIV

        if self.is_sphere:
            sphere_radius = max(self.bottom_radius, self.top_radius)

        bottom_point = [
            self.base_point[0],
            (
                self.base_point[1] - self.bottom_radius
                if not self.is_sphere
                else self.base_point[1] - sphere_radius
            ),
            self.base_point[2],
        ]
        top_point = [
            self.base_point[0],
            (
                self.base_point[1] + self.bottom_radius + self.top_radius
                if not self.is_sphere
                else self.base_point[1] + sphere_radius
            ),
            self.base_point[2],
        ]

        for i in range(1, self._SUBDIV):
            y = (abs(top_point[1] - bottom_point[1]) / self._SUBDIV) * i + bottom_point[
                1
            ]
            radius = (
                self.get_ovus_radius(y)
                if not self.is_sphere
                else self.get_radius(sphere_radius, y - self.base_point[1])
            )

            for j in range(self._SUBDIV):
                self.vertexes.append(
                    [
                        self.base_point[0] + radius * cos(circ_sub * j),
                        -y,
                        self.base_point[2] + radius * sin(circ_sub * j),
                    ]
                )

        bottom_point[1], top_point[1] = (
            -bottom_point[1],
            -top_point[1],
        )

        self.vertexes.insert(0, bottom_point)
        self.vertexes.append(top_point)

        # Edges
        for i in range(self._SUBDIV):
            self.edges.append((0, (i + 1)))
            for j in range(self._SUBDIV - 2):
                self.edges.append(
                    ((i + 1) + j * self._SUBDIV, (i + 1) + (j + 1) * self._SUBDIV)
                )
            self.edges.append(((i + 1) + (j + 1) * self._SUBDIV, -1))

        for j in range(self._SUBDIV - 1):
            for i in range(self._SUBDIV - 1):
                self.edges.append((i + 1 + j * self._SUBDIV, i + 2 + j * self._SUBDIV))
            self.edges.append(((j + 1) * self._SUBDIV, 1 + j * self._SUBDIV))

    def draw_on(self, views):
        for view in ["xy", "zy", "zx"]:
            root = views[view]["canvas"].get_root_item()
            GooCanvas.CanvasPath(
                parent=root,
                data=self.to_svg(view),
                line_width=1,
                stroke_color=LINE_COLOR,
                fill_color=None,
            )
