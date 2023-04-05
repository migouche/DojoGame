# vectors.py
# This file contains Vector2 and Vector2Int classes.
# This file contains all vector related calculations.

import random
import math

from dojogame.maths.dojomathfunctions import Mathf
from dojogame.maths.matrix import Matrix
from dojogame.maths.numba.vectors import JITVecs


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, v: 'Vector2'):
        return Vector2.from_tuple(JITVecs.add(*self, *v)) # if __getitem__() is defined you can unpack it, neat

    def __sub__(self, v: 'Vector2'):
        return Vector2.from_tuple(JITVecs.sub(*self, *v))

    def __neg__(self):
        return Vector2.from_tuple(JITVecs.neg(*self))

    def __mul__(self, f: float | int):
        return Vector2.from_tuple(JITVecs.mul(*self, f))

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, f):
        return Vector2.from_tuple(JITVecs.div(*self, f))

    def __str__(self):
        return "Vector2:(" + str(self.x) + ", " + str(self.y) + ")"

    def __eq__(self, v):
        return self.x == v.x and self.y == v.y

    def __iter__(self):
        return iter((self.x, self.y))

    def __getitem__(self, item):
        return (self.x, self.y)[item]

    def to_tuple(self) -> tuple:
        return self.x, self.y

    @staticmethod
    def from_tuple(t: tuple|list):
        return Vector2(t[0], t[1])

    @staticmethod
    def zero():
        return Vector2(0, 0)

    @staticmethod
    def dot(a, b) -> float:
        return JITVecs.dot(*a, *b)

    @staticmethod
    def cross(a, b) -> float:
        return JITVecs.cross(*a, *b)

    @staticmethod
    def scale(a, b):
        return Vector2.from_tuple(JITVecs.scale(*a, *b))

    @staticmethod
    def angle_rad(a, b) -> float:
        return JITVecs.angle(*a, *b)

    @staticmethod
    def angle_deg(a, b):
        return JITVecs.angle_deg(*a, *b)

    def to_vector2_int(self):
        return Vector2Int(*self) # the unpack operator is just too cool

    def magnitude(self):
        return JITVecs.mag(*self)

    def left_perpendicular(self):
        return Vector2(self.y, -self.x)

    def right_perpendicular(self):
        return Vector2(-self.y, self.x)

    @staticmethod
    def distance(a, b):
        return JITVecs.dist(*a, *b)

    def normalized(self):
        return Vector2.from_tuple(JITVecs.norm(*self))

    @staticmethod
    def from_angle_rad(angle):
        return Vector2(math.cos(angle), math.sin(angle))

    @staticmethod
    def from_angle_deg(angle):
        return Vector2.from_angle_rad(angle * Mathf.Deg2Rad)

    @staticmethod
    def random():
        return Vector2.rad_random(0, 6.28)

    @staticmethod
    def deg_random(a, b):
        return Vector2.rad_random(a * Mathf.Deg2Rad, b * Mathf.Deg2Rad)

    @staticmethod
    def rad_random(a, b):
        return Vector2.from_angle_rad(random.randint(int(a * 100), int(b * 100)) / 100).normalized()

    @staticmethod
    def rotate_by_rads(v, r):
        return Vector2(int((v.x * math.cos(r) - v.y * math.sin(r)) * 1000) / 1000,
                       int((v.x * math.sin(r) + v.y * math.cos(r)) * 1000) / 1000)

    @staticmethod
    def rotate_by_degs(v, d):
        return Vector2.rotate_by_rads(v, d * Mathf.Deg2Rad)

    def to_matrix_column(self) -> Matrix:
        return Matrix([[self.x], [self.y]])

    def to_matrix_row(self, z: float = 0) -> Matrix:
        return Matrix([[self.x, self.y, z]])

    @staticmethod
    def from_matrix(m: Matrix) -> 'Vector2':
        if (m.rows == 2 or m.rows == 3) and m.columns == 1:
            return Vector2(m.get_element(0, 0), m.get_element(1, 0))
        raise ValueError("Matrix must be 2x1 or 3x1 to be converted to Vector2")


class Vector2Int:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
    def __getitem__(self, item):
        return (self.x, self.y)[item]

    def __iter__(self):
        return iter((self.x, self.y))

    def __add__(self, v):
        return Vector2Int.from_tuple(JITVecs.add(*self, *v))

    def __sub__(self, v):
        return Vector2Int.from_tuple(JITVecs.sub(*self, *v))

    def __mul__(self, f):
        return Vector2Int.from_tuple(JITVecs.mul(*self, f))

    def __truediv__(self, f):
        return Vector2Int.from_tuple(JITVecs.div(*self, f))

    def __neg__(self):
        return Vector2Int.from_tuple(JITVecs.neg(*self))

    def __str__(self):
        return "Vector2Int:(" + str(self.x) + ", " + str(self.y) + ")"

    def __eq__(self, v):
        return self.x == v.x and self.y == v.y

    def to_tuple(self) -> tuple:
        return self.x, self.y

    @staticmethod
    def from_tuple(t: tuple[int]|list[int]):
        return Vector2Int(t[0], t[1])

    @staticmethod
    def zero():
        return Vector2(0, 0)

    def magnitude(self):
        return JITVecs.mag(*self)

    @staticmethod
    def distance(a, b):
        return (b - a).magnitude()

    def normalized(self):
        return Vector2Int.from_tuple(JITVecs.norm(*self))
