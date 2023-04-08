import pygame.surface

from dojogame import *
from pygame.constants import *
from numba import njit, prange
import numpy as np

'''this is a test of the mandelbrot set, it is necessary to import numpy for this one'''

'''if you are reading this second comment it's because i haven't implemented this stuff onto the engine
like all the stuff about surfarrays and blit_arrays, for now i use a hacky workaround with late_update'''

game = DojoGame()


def config():
    game.config_window(640, 480, "Fractals")


res = width, height = 640, 480
offset = np.array([1.3 * width, height]) // 2
increment = np.array([0.0, 0.0])
scale = .993
vel = .01
zoom = 2.2 / height
max_iter = 64

screen_array = np.full((640, 480, 3), [0, 0, 0], dtype=np.uint8)

texture = pygame.image.load("data/mandelbrottex1.bmp")
texture_size = min(texture.get_size()) - 1
texture_array = pygame.surfarray.pixels3d(texture)


@njit(fastmath=True, parallel=True)
def render(sa, _zoom, _offset, dx, dy, _max_iter):
    for x in prange(width):
        for y in range(height):
            c = (x - _offset[0]) * _zoom - dx + 1j * ((y - _offset[1]) * _zoom - dy)
            z = 0
            num_iter = 0
            for i in range(_max_iter):
                z = z ** 2 + c
                if z.real * z.real + z.imag * z.imag > 4:
                    break
                num_iter += 1
            col = int(texture_size * num_iter / _max_iter)
            sa[x, y] = texture_array[col, col]
    return sa


def start():
    RealTime.set_framerate(1000)


def update():
    global zoom, scale, vel, increment, max_iter
    if Input.get_key_down(K_ESCAPE) or Input.get_key_down(K_q):
        game.quit()

    if Input.get_key(K_a):
        increment[0] += vel * RealTime.delta_time * 15
    if Input.get_key(K_d):
        increment[0] -= vel * RealTime.delta_time * 15
    if Input.get_key(K_w):
        increment[1] += vel * RealTime.delta_time * 15
    if Input.get_key(K_s):
        increment[1] -= vel * RealTime.delta_time * 15

    if Input.get_key(K_UP) or Input.get_key(K_DOWN):
        inv_scale = 2 - scale
        if Input.get_key(K_UP):
            zoom *= scale
            vel *= scale
        if Input.get_key(K_DOWN):
            zoom *= inv_scale
            vel *= inv_scale

    if Input.get_key_down(K_PLUS):
        max_iter += 1
    if Input.get_key_down(K_MINUS):
        max_iter -= 1

    if Input.get_key_down(K_SPACE):
        print("FPS:", RealTime.clock.get_fps(), "zoom:", zoom, "offset:", offset, "increment:", increment, "max_iter:", max_iter)


    game.window.set_title(f"Fractals. FPS: {RealTime.clock.get_fps()}")


def late_update():
    global screen_array
    screen_array = render(screen_array, zoom, offset, increment[0], increment[1], max_iter)
    pygame.surfarray.blit_array(game.window.screen, screen_array)


game.run()
