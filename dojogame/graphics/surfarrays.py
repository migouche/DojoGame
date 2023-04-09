# surfarrays.py


from dojogame.graphics.drawable import Drawable
from numpy import ndarray
from pygame import surfarray


class Surfarray(Drawable):
    def __init__(self, arr: str | ndarray):
        super().__init__(True)
        if type(arr) is str:
            self.surface = surfarray.make_surface(arr)
        else:
            self.surface = surfarray.make_surface(arr)
