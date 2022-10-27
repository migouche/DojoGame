# enums.py

from enum import Enum

class ForceMode(Enum):
    Force = 1
    Acceleration = 2
    Impulse = 3
    VelocityChange = 4


class Space(Enum):
    World = 1
    Self = 2