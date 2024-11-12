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

# __     __        ____
# \ \   / /__  ___|___ \
#  \ \ / / _ \/ __| __) |
#   \ V /  __/ (__ / __/
#    \_/ \___|\___|_____|
#

class Vec2:
    def __init__(self, new_x, new_y = None):
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
    def __init__(self, new_x, new_y = None, new_z = None):
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
        return f'(Vec3) x: {self._x:g}, y: {self._y:g}, z: {self._z:g}'


    def __abs__(self):
        return self.mag()


    def __sub__(self, v2):                  # Operator overload (*)
        assert isinstance(v2, Vec3)
        return Vec3(self._x - v2._x,
                    self._y - v2._y,
                    self._z - v2._z)


    def __add__(self, v2):                  # Operator overload (+)
        assert isinstance(v2, Vec3)
        return Vec3(self._x + v2._x,
                    self._y + v2._y,
                    self._z + v2._z)


    def __mul__(self, v2):                  # Operator overload (* = dot)
        if isinstance(v2, Number):
            return Vec3(self._x * v2,
                        self._y * v2,
                        self._z * v2)
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
        return Vec3(self._y * v2.z - self._z * v2.y,
                    self._z * v2.x - self._x * v2.z,
                    self._x * v2.y - self._y * v2.x)


    def normalized(self):
        d = self.mag()
        return Vec3(self._x/d, self._y/d, self._z/d)


    def mag(self):
        return sqrt(self._x**2 + self._y**2 + self._z**2)

# __     __        _  _
# \ \   / /__  ___| || |
#  \ \ / / _ \/ __| || |_
#   \ V /  __/ (__|__   _|
#    \_/ \___|\___|  |_|
#

class Vec4:
    def __init__(self, new_x, new_y = None, new_z = None, new_w = None):
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
        return f'(Vec3) x: {self._x:g}, y: {self._y:g}, z: {self._z:g}, z: {self._w:g}'



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
        self.hits = []
        
        
    def add_hit(self, hit):
        self.hits.append(hit)
        
        
    def nearest_hit(self):
        t_hits = [hit.t for hit in self.hits]
        return self.hits[t_hits.index(min(t_hits))]

#  ____   ____ ____
# |  _ \ / ___| __ )
# | |_) | |  _|  _ \
# |  _ <| |_| | |_) |
# |_| \_\\____|____/
#

class RGB:
    def __init__(self, r, g = None, b = None):
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
#
#  ____   ____ ____    _
# |  _ \ / ___| __ )  / \
# | |_) | |  _|  _ \ / _ \
# |  _ <| |_| | |_) / ___ \
# |_| \_\\____|____/_/   \_\
#

class RGBA:
    def __init__(self, r, g, b, a):
        self.r, self.g, self.b, self.a = r, g, b, a


#  _     _ _                            _            _
# | |   (_) |__  _ __ __ _ _ __ _   _  | |_ ___  ___| |_ ___
# | |   | | '_ \| '__/ _` | '__| | | | | __/ _ \/ __| __/ __|
# | |___| | |_) | | | (_| | |  | |_| | | ||  __/\__ \ |_\__ \
# |_____|_|_.__/|_|  \__,_|_|   \__, |  \__\___||___/\__|___/
#                               |___/

def test_Vec3():
    for test in ["Vec3(1.11, 2.22, 3.33)",
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
                 "(Vec3(1, 2, 3) - Vec3(4, 5, 6)) * 3"]:
        print(f'{test} --> {str(eval(test))}')


def test_Ray():
    for test in ["Ray(Vec3(1, 2, 3), Vec3(4, 5, 6))",
                 "Ray(Vec3(1, 2, 3), Vec3(4, 5, 6)).at(2)"]:
        print(f'{test} --> {str(eval(test))}')
        
        
def test_hit_list():
    lst = Hit_list()
    lst.add_hit(Hit(None, 1.23))
    lst.add_hit(Hit(None, -1.23))
    lst.add_hit(Hit(None, 1.24))
    lst.add_hit(Hit(None, 10.23))
    print('Least: ', lst.nearest_hit().t)
    


def main(args):
    # ~ test_Vec3()
    # ~ test_Ray()
    test_hit_list()
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
