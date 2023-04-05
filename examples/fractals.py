import pygame.surface

from dojogame import *
from pygame.constants import *
from numba import njit, prange

# define array for all colors in color depth 3:
Rs = [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
      255,
      255,
      255,
      236,
      217,
      198,
      179,
      160,
      141,
      122,
      103,
      84,
      65,
      46,
      27,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      21,
      42,
      63,
      84,
      105,
      126,
      147,
      168,
      189,
      210,
      231,
      255,
      0
      ]
Gs = [
    0,
    19,
    38,
    57,
    76,
    95,
    114,
    133,
    152,
    171,
    190,
    209,
    228,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    236,
    217,
    198,
    179,
    160,
    141,
    122,
    103,
    84,
    65,
    46,
    27,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
]
Bs = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    21,
    42,
    63,
    84,
    105,
    126,
    147,
    168,
    189,
    210,
    231,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    255,
    0
]

print(len(Rs), len(Gs), len(Bs))


# -----------------------------------------------------------------------------------------------------
@njit(fastmath=True)
def get_complex(x, y):
    return x / 160 - 2.5, y / 160 - 1.5


@njit(fastmath=True)
def add_complex(r1, i1, r2, i2):
    return r1 + r2, i1 + i2


@njit(fastmath=True)
def mul_complex(r1, i1, r2, i2):
    return r1 * r2 - i1 * i2, r1 * i2 + i1 * r2


@njit(fastmath=True, parallel=True)
def mandelbrot_it(r, i, max_iter=64):
    zr = 0
    zi = 0
    for j in range(max_iter):
        zr, zi = add_complex(*mul_complex(zr, zi, zr, zi), r, i)
        if zr * zr + zi * zi > 4:
            return j
    return max_iter


game = DojoGame()
fractal: pygame.pixelarray.PixelArray = None
surface: pygame.surface.Surface = None


def config():
    game.config_window(640, 480, "Fractals")


def start():
    global fractal, surface

    surface = pygame.Surface((game.window.width, game.window.height))
    fractal = pygame.pixelarray.PixelArray(surface)


def update():
    global fractal, surface
    if Input.get_key_down(K_ESCAPE) or Input.get_key_down(K_q):
        game.quit()


def late_update():
    global fractal, surface
    for x in range(game.window.width):
        for y in range(game.window.height):
            i = mandelbrot_it(*get_complex(x, y))
            fractal[x, y] = (Rs[i], Gs[i], Bs[i])
    print(RealTime.clock.get_fps())

    game.window.screen.blit(fractal.surface.copy(), (0, 0))


game.run()
