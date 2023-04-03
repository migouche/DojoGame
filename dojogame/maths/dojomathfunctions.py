import math
import sys
from sys import float_info


class Mathf:
    @staticmethod
    def clamp(value, Min, Max):
        if value <= Min:
            return Min
        elif value >= Max:
            return Max
        else:
            return value

    @staticmethod
    def is_between(val: float, x: float, y: float) -> bool:
        _x, _y = min(x, y), max(x, y)
        return _x <= val <= _y

    @staticmethod
    def sign(x) -> int:
        return -1 if x < 0 else 1

    Deg2Rad = math.pi / 180
    Rad2Deg = 1 / Deg2Rad
    epsilon = float_info.epsilon
