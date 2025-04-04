# window.py

from dojogame.graphics.colors import Colors
from dojogame.inputs import Input, Button  # Need to import it
from dojogame.data import arrays
from dojogame.maths.realtime import RealTime

from pygame.constants import QUIT
import pygame.display

import time


class Window:
    def __init__(self, width: int = 0, height: int = 0, title: str = "Game Window", icon: str = None,
                 flags: list[int] | int = 0,
                 depth: int = 0, display: int = 0, vsync: bool = False):

        Input.update()
        self.running = True
        totalFlags = 0
        self.debug_time = 0
        if type(flags) is not int:
            for flag in flags:
                totalFlags |= flag
        else:
            totalFlags = flags

        self.screen = pygame.display.set_mode((width, height), totalFlags, depth, display, 1 if vsync else 0)
        self.width, self.height = pygame.display.get_window_size()
        self.icon = icon
        self.title = title
        if icon is not None:
            self.set_icon(icon)
        self.set_title(title)

        self.bgColor = Colors.white
        Input.update()  # can't figure out why I need 2 Input.Update(). It just works like that

    def fill_bg(self, color):
        if self.running:
            self.screen.fill(color.to_tuple())

    def set_bg(self, color):
        self.bgColor = color

    def set_title(self, title):
        self.title = title
        pygame.display.set_caption(title)

    def set_icon(self, icon):
        self.icon = pygame.image.load(icon)
        pygame.display.set_icon(self.icon)

    def update(self):
        if self.running:
            self.width, self.height = pygame.display.get_window_size()
            if Input.get_event(QUIT):
                self.quit()
                return

            self.fill_bg(self.bgColor)

            screen_temp = pygame.Surface((self.width, self.height))
            screen_temp.fill(self.bgColor.to_tuple())

            for drawable in arrays.drawables:
                drawable.update(screen_temp)
                if not drawable.persistent:
                    arrays.drawables.remove(drawable)

            self.screen.blit(screen_temp, (0, 0))

            Input.update()
            #pygame.display.flip()
            #s = time.time()
            #RealTime.tick()
            #self.debug_time = (time.time() - s) / (1 / RealTime.fps) * 100

    def late_update(self):
        if self.running:
            pygame.display.flip()
            s = time.time()
            RealTime.tick()
            self.debug_time = (time.time() - s) / (1 / RealTime.fps) * 100

    def quit(self):
        self.running = False
        pygame.quit()
