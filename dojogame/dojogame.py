# dojogame.py
# This file contains the base of the engine.
# This file acts as a link between all submodules

from dojogame.dojophysics import *
from dojogame.dojographics import *
from dojogame.dojodata import *
from dojogame import dojoconstants


def init():
    pygame.init()
    Input.update()
