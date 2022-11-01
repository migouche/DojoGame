# colors.py

class Color:
    def __init__(self, r: int, g: int, b: int, a: int = 255):
        self.red = r
        self.green = g
        self.blue = b
        self.alpha = a

    def __eq__(self, c):
        return self.red == c.red and\
               self.green == c.green and\
               self.blue == c.blue and\
               self.alpha == c.alpha

    @staticmethod
    def from_hex(h):
        c = tuple(int(h.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
        return Color(c[0], c[1], c[2])

    def to_tuple(self):
        return self.red, self.green, self.blue, self.alpha


class Colors:
    white = Color(255, 255, 255)
    black = Color(0, 0, 0)
    red = Color(255, 0, 0)
    green = Color(0, 255, 0)
    blue = Color(0, 0, 255)
    purple = Color(100, 0, 255)
    transparent = Color(0, 0, 0, 0)


Colour = Color
Colours = Colors
