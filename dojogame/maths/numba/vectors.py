# numba/vectors.py
# This file contains optimized vector calculations.

import math
from numba import njit
class JITVecs:
    @staticmethod
    @njit
    def add(x1, y1, x2, y2):  # just unpack them when calling
        return x1 + x2, y1 + y2

    @staticmethod
    @njit
    def sub(x1, y1, x2, y2):
        return x1 - x2, y1 - y2

    @staticmethod
    @njit
    def mul(x, y, f):
        return x * f, y * f

    @staticmethod
    @njit
    def div(x, y, f):
        return x / f, y / f

    @staticmethod
    @njit
    def neg(x, y):
        return -x, -y

    @staticmethod
    @njit
    def dot(x1, y1, x2, y2):
        return x1 * x2 + y1 * y2

    @staticmethod
    @njit
    def cross(x1, y1, x2, y2):
        return x1 * y2 - y1 * x2

    @staticmethod
    @njit
    def scale(x1, y1, x2, y2):
        return x1 * x2, y1 * y2

    @staticmethod
    @njit
    def mag(x, y) -> float:
        return math.sqrt(x * x + y * y)

    @staticmethod
    @njit
    def norm(x, y):
        mag = math.sqrt(x * x + y * y)  # can't use JITVecs.mag() here
        return x / mag, y / mag

    @staticmethod
    @njit
    def dist(x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    @staticmethod
    @njit
    def angle(x1, y1, x2, y2):
        return math.atan2(y2 - y1, x2 - x1)

    @staticmethod
    @njit
    def angle_deg(x1, y1, x2, y2):
        return math.degrees(math.atan2(y2 - y1, x2 - x1))


