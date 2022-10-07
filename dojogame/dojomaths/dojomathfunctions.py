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

    Deg2Rad = math.pi / 180
    Rad2Deg = 1 / Deg2Rad
    epsilon = float_info.epsilon
