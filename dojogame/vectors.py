import random
import math
import sys

sys.path.append("")

from dojogame.dojomathfunctions import *

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, v):
        return Vector2(self.x + v.x, self.y + v.y)

    def __sub__(self, v):
        return Vector2(self.x - v.x, self.y - v.y)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __mul__(self, f):
        return Vector2(self.x * f, self.y * f)

    def __truediv__(self, f):
        return Vector2(self.x / f, self.y / f)

    def __str__(self):
        return "Vector2:(" + str(self.x) + ", " + str(self.y) + ")"

    def __eq__(self, v):
        return self.x == v.x and self.y == v.y

    def to_tuple(self) -> tuple:
        return self.x, self.y

    @staticmethod
    def zero():
        return Vector2(0, 0)

    @staticmethod
    def dot(a, b) -> float:
        return a.x * b.x + a.y * b.y

    @staticmethod
    def cross(a, b) -> float:
        return a.x * b.y - b.x * a.y

    @staticmethod
    def scale(a, b):
        return Vector2(a.x * b.x, a.y * b.y)

    @staticmethod
    def angle_rad(a, b) -> float:
        return math.atan2(Vector2.cross(a, b), Vector2.dot(a, b))

    @staticmethod
    def angle_deg(a, b):
        return Vector2.angle_rad(a, b) * Mathf.Rad2Deg

    def to_vector2_int(self):
        return Vector2Int(int(self.x), int(self.y))

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

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


class Vector2Int:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __add__(self, v):
        return Vector2Int(self.x + v.x, self.y + v.y)

    def __sub__(self, v):
        return Vector2Int(self.x - v.x, self.y - v.y)

    def __mul__(self, f):
        return Vector2Int(self.x * f, self.y * f)

    def __truediv__(self, f):
        return Vector2Int(self.x / f, self.y / f)

    def __str__(self):
        return "Vector2Int:(" + str(self.x) + ", " + str(self.y) + ")"

    def __eq__(self, v):
        return self.x == v.x and self.y == v.y

    @staticmethod
    def zero():
        return Vector2(0, 0)

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    @staticmethod
    def distance(a, b):
        return (b - a).magnitude()

    def normalized(self):
        return self / self.magnitude()
