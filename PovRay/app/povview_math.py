from math import cos, sin, pi, sqrt
from pdb import set_trace as st
from numbers import Number

import numpy as np

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

        elif (
            isinstance(new_x, list)
            or isinstance(new_x, tuple)
            or isinstance(new_x, np.ndarray)
        ):
            assert len(new_x) == 2
            assert new_y == None

            self._x, self._y = new_x

        else:
            assert new_y != None
            self._x, self._y = new_x, new_y

    def __str__(self):
        return f"Vec2({self._x}, {self._y})"

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, index):
        return [self._x, self._y][index]

    def __setitem__(self, index, value):
        match index:
            case 0:
                self._x = value
            case 1:
                self._y = value
            case _:
                raise IndexError

    @property
    def __array__(self) -> np.ndarray:
        return np.array([self._x, self._y])


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

        elif (
            isinstance(new_x, list)
            or isinstance(new_x, tuple)
            or isinstance(new_x, np.ndarray)
        ):
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
        return f"Vec3({self._x}, {self._y}, {self._z})"

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, index):
        return [self._x, self._y, self._z][index]

    def __setitem__(self, index, value):
        match index:
            case 0:
                self._x = value
            case 1:
                self._y = value
            case 2:
                self._z = value
            case _:
                raise IndexError

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

    @property
    def __array__(self) -> np.ndarray:
        return np.array([self._x, self._y, self._z])

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

    @staticmethod
    def min(v1, v2):
        return Vec3(min(v1.x, v2.x), min(v1.y, v2.y), min(v1.z, v2.z))

    @staticmethod
    def max(v1, v2):
        return Vec3(max(v1.x, v2.x), max(v1.y, v2.y), max(v1.z, v2.z))


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

        elif (
            isinstance(new_x, list)
            or isinstance(new_x, tuple)
            or isinstance(new_x, np.ndarray)
        ):
            assert len(new_x) == 4
            assert (new_y == None) and (new_z == None) and (new_w == None)

            self._x, self._y, self._z, self._w = new_x

        else:
            assert (new_y != None) and (new_z != None) and (new_w != None)

            self._x, self._y, self._z, self._w = new_x, new_y, new_z, new_w

    def __str__(self):
        return f"Vec4({self._x}, {self._y}, {self._z}, {self._w})"

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, index):
        return [self._x, self._y, self._z, self._w][index]

    def __setitem__(self, index, value):
        match index:
            case 0:
                self._x = value
            case 1:
                self._y = value
            case 2:
                self._z = value
            case 3:
                self._w = value
            case _:
                raise IndexError

    @property
    def __array__(self) -> np.ndarray:
        return np.array([self._x, self._y, self._z, self._w])

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
        return f"RGB(r: {self._rgb[0]}, g: {self._rgb[1]}, b: {self._rgb[2]})"

    def __repr__(self):
        return self.__str__()

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
        return f"RGBA(r: {self._rgba[0]}, g: {self._rgba[1]}, b: {self._rgba[2]}, a: {self._rgba[3]})"

    def __repr__(self):
        return self.__str__()

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
    def __init__(self, origin, direction):
        assert isinstance(origin, Vec3)
        assert isinstance(direction, Vec3)

        self.origin = origin
        self.direction = direction

    def __str__(self):
        return f"Ray(origin: {self.origin}, direction: {self.direction})"

    def __repr__(self):
        return self.__str__()

    def at(self, t):
        return self.origin + self.direction * t


#   _    _ _ _
#  | |  | (_) |
#  | |__| |_| |_
#  |  __  | | __|
#  | |  | | | |_
#  |_|  |_|_|\__|


class Hit:
    def __init__(self, obj, t):
        self.obj, self.t = obj, t

    def __str__(self):
        return f"Hit(obj: {self.obj}, t: {self.t})"

    def __repr__(self):
        return self.__str__()


#   _    _ _ _   _      _     _
#  | |  | (_) | | |    (_)   | |
#  | |__| |_| |_| |     _ ___| |_
#  |  __  | | __| |    | / __| __|
#  | |  | | | |_| |____| \__ \ |_
#  |_|  |_|_|\__|______|_|___/\__|


class HitList:
    def __init__(self):
        self.clear()

    def __str__(self):
        return f"HitList[{', '.join(str(hit) for hit in self.hits)}]"

    def __repr__(self):
        return self.__str__()

    def append(self, hit):
        self.hits.append(hit)

    def empty(self):
        self.hits == []

    def nearest_hit(self):
        return min(self.hits, key=lambda x: x.t)

    def clear(self):
        self.hits = []


#   _______   _                   _
#  |__   __| (_)                 | |
#     | |_ __ _  __ _ _ __   __ _| | ___
#     | | '__| |/ _` | '_ \ / _` | |/ _ \
#     | | |  | | (_| | | | | (_| | |  __/
#     |_|_|  |_|\__,_|_| |_|\__, |_|\___|
#                            __/ |
#                           |___/


class Triangle:
    def __init__(self, new_a, new_b=None, new_c=None):
        if isinstance(new_a, Triangle):
            assert new_b == None
            assert new_c == None

            self._a, self._b, self._c = new_a._a, new_a._b, new_a._c

        elif isinstance(new_a, list) or isinstance(new_a, tuple):
            assert len(new_a) == 3
            assert new_b == None
            assert new_c == None

            self._a, self._b, self._c = new_a[0], new_a[1], new_a[2]

        else:
            assert new_b != None
            assert new_c != None

            self._a, self._b, self._c = new_a, new_b, new_c

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b

    @property
    def c(self):
        return self._c

    def __str__(self):
        return f"Triangle(a: {self._a}, b: {self._b}, c: {self._c})"

    def __repr__(self):
        return self.__str__()

    def intersection(self, ray: Ray):
        edge1 = self._b - self._a
        edge2 = self._c - self._a
        h = ray.direction.cross(edge2)
        a = edge1.dot(h)

        if -1e-5 < a < 1e-5:  # Rayo paralelo al triángulo
            return None

        f = 1 / a
        s = ray.origin - self._a
        u = f * s.dot(h)

        if u < 0.0 or u > 1.0:
            return None

        q = s.cross(edge1)
        v = f * ray.direction.dot(q)

        if v < 0.0 or u + v > 1.0:
            return None

        t = f * edge2.dot(q)
        if t > 1e-5:
            return t
        return None
