# vectors.py
# This file contains Vector2 and Vector2Int classes.
# This file contains all vector related calculations.

import random
from math import atan2, sin, cos

from dojogame.maths.dojomathfunctions import Mathf
from dojogame.maths.matrix import Matrix


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, v: 'Vector2'):
        return Vector2(x=self.x + v.x, y=self.y + v.y)

    def __sub__(self, v: 'Vector2'):
        return Vector2(x=self.x - v.x, y=self.y - v.y)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __mul__(self, f: float | int):
        return Vector2(x=self.x * f, y=self.y * f)

    def __rmul__(self, other: float | int):
        return self * other

    def __truediv__(self, f: float | int):
        return Vector2(x=self.x / f, y=self.y / f)

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
    def from_tuple(t: tuple | list):
        return Vector2(t[0], t[1])

    @staticmethod
    def zero():
        return Vector2(0, 0)

    @staticmethod
    def dot(a, b) -> float:
        return a.x * b.x + a.y * b.y

    @staticmethod
    def cross(a, b) -> float:
        return a.x * b.y - a.y * b.x

    @staticmethod
    def scale(a, b):
        return Vector2(a.x * b.x, a.y * b.y)

    @staticmethod
    def angle_rad(a, b) -> float:
        return atan2(Vector2.cross(a, b), Vector2.dot(a, b))

    @staticmethod
    def angle_deg(a, b):
        return Vector2.angle_rad(a, b) * Mathf.Rad2Deg

    def to_vector2_int(self):
        return Vector2Int(*self)  # the unpack operator is just too cool

    def magnitude(self):
        return self.x ** 2 + self.y ** 2

    def left_perpendicular(self):
        return Vector2(self.y, -self.x)

    def right_perpendicular(self):
        return Vector2(-self.y, self.x)

    @staticmethod
    def distance(a, b):
        return (b - a).magnitude()

    def normalized(self):
        return self / self.magnitude()

    @staticmethod
    def from_angle_rad(angle):
        return Vector2(cos(angle), sin(angle))

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
        return Vector2(int((v.x * cos(r) - v.y * sin(r)) * 1000) / 1000,
                       int((v.x * sin(r) + v.y * cos(r)) * 1000) / 1000)

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
        return Vector2Int(self.x + v.x, self.y + v.y)

    def __sub__(self, v):
        return Vector2Int(self.x - v.x, self.y - v.y)

    def __mul__(self, f):
        return Vector2Int(self.x * f, self.y * f)

    def __truediv__(self, f):
        return Vector2Int(self.x / f, self.y / f)

    def __neg__(self):
        return Vector2Int(-self.x, -self.y)

    def __str__(self):
        return "Vector2Int:(" + str(self.x) + ", " + str(self.y) + ")"

    def __eq__(self, v):
        return self.x == v.x and self.y == v.y

    def to_tuple(self) -> tuple:
        return self.x, self.y

    @staticmethod
    def from_tuple(t: tuple[int] | list[int]):
        return Vector2Int(t[0], t[1])

    @staticmethod
    def zero():
        return Vector2(0, 0)

    def magnitude(self):
        return self.x ** 2 + self.y ** 2

    @staticmethod
    def distance(a, b):
        return (b - a).magnitude()

    def normalized(self):
        return Vector2Int(self.x / self.magnitude(), self.y / self.magnitude())
