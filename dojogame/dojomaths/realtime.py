# realtime.py

import pygame.time


class RealTime:
    clock = pygame.time.Clock()
    fps = 60
    delta_time = 1 / 60

    @staticmethod
    def init():
        RealTime.clock = pygame.time.Clock()
        RealTime.fps = 60

    @staticmethod
    def set_framerate(fps):
        RealTime.fps = fps
        RealTime.delta_time = 1 / fps

    @staticmethod
    def tick():
        RealTime.clock.tick_busy_loop(RealTime.fps)
        try:
            RealTime.delta_time = 1 / RealTime.clock.get_fps()
        except ZeroDivisionError:
            pass
