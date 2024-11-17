#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  povview_math.py
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

from math import cos, sin, pi, sqrt
from pdb import set_trace as st
from numbers import Number

COLORS = {
    "Black": [0, 0, 0],
    "White": [1, 1, 1],
    "Red": [1, 0, 0],
    "DarkRed": [0.5, 0, 0],
    "Green": [0, 1, 0],
    "DarkGreen": [0, 0.5, 0],
    "Blue": [0, 0, 1],
    "DarkBlue": [0, 0, 0.5],
    "Yellow": [1, 1, 0],
    "Purple": [1, 0, 1],
    "Cyan": [0, 1, 1],
    "Orange": [1, 0.5, 0],
    "Salmon": [0.98, 0.5, 0.447],
    "Rosa": [1, 0.75, 0.8],
    "Coral": [1, 0.5, 0.313],
    "Gold": [1, 215, 0.81],
    "Violet": [0.93, 0.51, 0.93],
    "Olive": [0.5, 0.5, 0],
    "Chocolate": [0.82, 0.41, 0.12],
    "Gray25": [0.25, 0.25, 0.25],
    "Gray": [0.5, 0.5, 0.5],
    "Gray75": [0.75, 0.75, 0.75],
}

# __     __        ____
# \ \   / /__  ___|___ \
#  \ \ / / _ \/ __| __) |
#   \ V /  __/ (__ / __/
#    \_/ \___|\___|_____|
#


class Vec2:
    def __init__(self, new_x, new_y=None):
        print(new_x, new_y)
        if isinstance(new_x, Vec2):
            assert new_y == None

            self._x, self._y = new_x._x, new_x._y

        elif isinstance(new_x, list) or isinstance(new_x, tuple):
            assert len(new_x) == 2
            assert new_y == None

            self._x, self._y = new_x

        else:
            assert new_y != None
            self._x, self._y = new_x, new_y


# __     __        _____
# \ \   / /__  ___|___ /
#  \ \ / / _ \/ __| |_ \
#   \ V /  __/ (__ ___) |
#    \_/ \___|\___|____/
#


class Vec3:
    def __init__(self, new_x, new_y=None, new_z=None):
        if isinstance(new_x, Vec3):
            assert new_y == None
            assert new_z == None

            self._x, self._y, self._z = new_x._x, new_x._y, new_x._z

        elif isinstance(new_x, list) or isinstance(new_x, tuple):
            assert len(new_x) == 3
            assert new_y == None
            assert new_z == None

            self._x, self._y, self._z = new_x[0], new_x[1], new_x[2]

        else:
            assert new_y != None
            assert new_z != None

            self._x, self._y, self._z = new_x, new_y, new_z

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    def __str__(self):
        return f"(Vec3: {self._x:g}, {self._y:g}, {self._z:g})"

    def __abs__(self):
        return self.mag()

    def __sub__(self, v2):  # Operator overload (*)
        assert isinstance(v2, Vec3)
        return Vec3(self._x - v2._x, self._y - v2._y, self._z - v2._z)

    def __add__(self, v2):  # Operator overload (+)
        assert isinstance(v2, Vec3)
        return Vec3(self._x + v2._x, self._y + v2._y, self._z + v2._z)

    def __mul__(self, v2):  # Operator overload (* = dot)
        if isinstance(v2, Number):
            return Vec3(self._x * v2, self._y * v2, self._z * v2)
        else:
            return self.dot(v2)

    def add(self, v2):
        assert isinstance(v2, Vec3)
        self._x += v2.x
        self._y += v2.y
        self._z += v2.z
        return self

    def sub(self, v2):
        assert isinstance(v2, Vec3)
        self._x -= v2.x
        self._y -= v2.y
        self._z -= v2.z
        return self

    def dot(self, v2):
        assert isinstance(v2, Vec3)
        return self._x * v2.x + self._y * v2.y + self._z * v2.z

    def cross(self, v2):
        assert isinstance(v2, Vec3)
        return Vec3(
            self._y * v2.z - self._z * v2.y,
            self._z * v2.x - self._x * v2.z,
            self._x * v2.y - self._y * v2.x,
        )

    def normalized(self):
        d = self.mag()
        return Vec3(self._x / d, self._y / d, self._z / d)

    def mag(self):
        return sqrt(self._x**2 + self._y**2 + self._z**2)


# __     __        _  _
# \ \   / /__  ___| || |
#  \ \ / / _ \/ __| || |_
#   \ V /  __/ (__|__   _|
#    \_/ \___|\___|  |_|
#


class Vec4:
    def __init__(self, new_x, new_y=None, new_z=None, new_w=None):
        if isinstance(new_x, Vec4):
            assert (new_y == None) and (new_z == None) and (new_w == None)

            self._x, self._y, self._z, self._w = new_x._x, new_x._y, new_x._z, new_x.w

        elif isinstance(new_x, list) or isinstance(new_x, tuple):
            assert len(new_x) == 4
            assert (new_y == None) and (new_z == None) and (new_w == None)

            self._x, self._y, self._z, self._w = new_x

        else:
            assert (new_y != None) and (new_z != None) and (new_w != None)

            self._x, self._y, self._z, self._w = new_x, new_y, new_z, new_w

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    @property
    def w(self):
        return self._w

    def __str__(self):
        return f"(Vec4) x: {self.x:g}, y: {self._y:g}, z: {self._z:g}, w: {self._w:g}"


#  ____   ____ ____
# |  _ \ / ___| __ )
# | |_) | |  _|  _ \
# |  _ <| |_| | |_) |
# |_| \_\\____|____/
#


class RGB:
    def __init__(self, r, g=None, b=None):
        if isinstance(r, list) or isinstance(r, tuple):
            self._rgb = r
        elif (g is None) and (b is None):
            self._rgb = [r, r, r]
        else:
            self._rgb = [r, g, b]

    def __str__(self):
        return f"(RBA) r: {self._rgb[0]}, g: {self._rgb[1]}, b: {self._rgb[2]}"

    def limit(self):
        for c in range(3):
            self._rgb[c] = min(self._rgb[c], 1)
            self._rgb[c] = max(self._rgb[c], 0)
        return self

    def __add__(self, c2):
        for c in range(3):
            self._rgb[c] += c2._rgb[c]
        return self

    def __sub__(self, c2):
        for c in range(3):
            self._rgb[c] -= c2._rgb[c]
        return self

    def __mul__(self, f):
        for c in range(3):
            self._rgb[c] *= f
        return self

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

    @property
    def as_rgb8(self):
        return (self._r * 255, self._g * 255, self._b * 255)


#
#  ____   ____ ____    _
# |  _ \ / ___| __ )  / \
# | |_) | |  _|  _ \ / _ \
# |  _ <| |_| | |_) / ___ \
# |_| \_\\____|____/_/   \_\
#


class RGBA:
    def __init__(self, r, g=None, b=None, a=None):
        if isinstance(r, list) or isinstance(r, tuple):
            assert len(r) == 4
            assert g is None
            assert b is None
            assert a is None
            self._rgba = r
        else:
            assert g is not None
            assert b is not None
            assert a is not None
            self._rgba = [r, g, b, a]

    def __str__(self):
        return (
            f"(RGBA) r: {self._rgba[0]}, "
            f"g: {self._rgba[1]}, "
            f"b: {self._rgba[2]}, "
            f"a: {self._rgba[3]}"
        )

    def limit(self):
        for c in range(4):
            self._rgba[c] = min(self._rgba[c], 1)
            self._rgba[c] = max(self._rgba[c], 0)
        return self

    def __add__(self, c2):
        for c in range(4):
            self._rgba[c] += c2._rgba[c]
        return self

    def __sub__(self, c2):
        for c in range(4):
            self._rgba[c] -= c2._rgba[c]
        return self

    def __mul__(self, f):
        for c in range(4):
            self._rgba[c] *= f
        return self

    @property
    def r(self):
        return self._rgba[0]

    @property
    def g(self):
        return self._rgba[1]

    @property
    def b(self):
        return self._rgba[2]

    @property
    def a(self):
        return self._rgba[3]

    @property
    def rgba(self):
        return self._rgba


#  ____
# |  _ \ __ _ _   _
# | |_) / _` | | | |
# |  _ < (_| | |_| |
# |_| \_\__,_|\__, |
#             |___/


class Ray:
    def __init__(self, location, direction):
        assert isinstance(location, Vec3)
        assert isinstance(direction, Vec3)

        self.location = location
        self.direction = direction

    def __str__(self):
        return f"loc: {self.location}, dir: {self.direction}"

    def at(self, t):
        return self.location + self.direction * t


class Hit:
    def __init__(self, obj, t):
        self.obj, self.t = obj, t


class Hit_list:
    def __init__(self):
        self.clear()

    def append(self, hit):
        self.hits.append(hit)

    def empty(self):
        self.hits == []

    def nearest_hit(self):
        nearest = Hit(None, float("inf"))
        for hit in self.hits:
            if hit.t < nearest.t:
                nearest = hit

        return nearest

    def clear(self):
        self.hits = []


#  _     _ _                            _            _
# | |   (_) |__  _ __ __ _ _ __ _   _  | |_ ___  ___| |_ ___
# | |   | | '_ \| '__/ _` | '__| | | | | __/ _ \/ __| __/ __|
# | |___| | |_) | | | (_| | |  | |_| | | ||  __/\__ \ |_\__ \
# |_____|_|_.__/|_|  \__,_|_|   \__, |  \__\___||___/\__|___/
#                               |___/


def test_Vec3():
    for test in [
        "Vec3(1.11, 2.22, 3.33)",
        "Vec3(Vec3(1.11, 2.22, 3.33))",
        "Vec3([1.11, 2.22, 3.33])",
        "Vec3((1.11, 2.22, 3.33))",
        "Vec3(1, 2, 3).mag()",
        "Vec3(1, 2, 3).normalized()",
        "Vec3(1, 2, 3).dot(Vec3(4, 5, 6))",
        "Vec3(1, 2, 3).add(Vec3(4, 5, 6))",
        "Vec3(1, 2, 3).sub(Vec3(4, 5, 6))",
        "Vec3(1, 2, 3).cross(Vec3(4, 5, 6))",
        "abs(Vec3(1, 2, 3))",
        "Vec3(1, 2, 3) + Vec3(4, 5, 6)",
        "(Vec3(1, 2, 3) + Vec3(4, 5, 6)) * 3",
        "Vec3(1, 2, 3) - Vec3(4, 5, 6)",
        "Vec3(1, 2, 3) * 3",
        "(Vec3(1, 2, 3) - Vec3(4, 5, 6)) * 3",
    ]:
        print(f"{test} --> {str(eval(test))}")


def test_Ray():
    for test in [
        "Ray(Vec3(1, 2, 3), Vec3(4, 5, 6))",
        "Ray(Vec3(1, 2, 3), Vec3(4, 5, 6)).at(2)",
    ]:
        print(f"{test} --> {str(eval(test))}")


def test_RGB():
    for test in [
        "RGB(0.1, 0.2, 0.3)",
        "RGB(0.1, 0.2, 0.3).limit()",
        "RGB(1.1, 1.2, 1.2).limit()",
        "RGB(-0.1, -0.2, -0.2).limit()",
        "RGB(0.1, 0.2, 0.3) * 2",
        "RGB(0.1, 0.2, 0.3) + RGB(0.15, 0.25, 0.35)",
        "RGB(0.1, 0.2, 0.3) - RGB(0.15, 0.25, 0.35)",
        "RGB(0.123)",
    ]:
        print(f"{test}\n --> {str(eval(test))}")


def test_RGBA():
    for test in [
        "RGBA(0.1, 0.2, 0.3, 0.4)",
        "RGBA(0.1, 0.2, 0.3, 0.4).limit()",
        "RGBA(1.1, 1.2, 1.2, 0.4).limit()",
        "RGBA(-0.1, -0.2, -0.2, -0.4).limit()",
        "RGBA(0.1, 0.2, 0.3, 0.4) * 2",
        "RGBA(0.1, 0.2, 0.3, 0.4) + RGBA(0.15, 0.25, 0.35, 0.45)",
        "RGBA(0.1, 0.2, 0.3, 0.4) - RGBA(0.15, 0.25, 0.35, 0.45)",
    ]:
        print(f"{test}\n --> {str(eval(test))}")


def test_hit_list():
    lst = Hit_list()
    lst.append(Hit(None, 1.23))
    lst.append(Hit(None, -1.23))
    lst.append(Hit(None, 1.24))
    lst.append(Hit(None, 10.23))
    print("Least: ", lst.nearest_hit().t)


def main(args):
    # ~ test_Vec3()
    # ~ test_Ray()
    # ~ test_RGB()
    # ~ test_RGBA()
    test_hit_list()
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))
