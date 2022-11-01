from typing import Union

from dojogame.graphics.colors import Colors
from dojogame.inputs import Input, Button
from dojogame.data import arrays
from dojogame.maths.realtime import RealTime

from pygame.constants import QUIT
import pygame.display


class Window:
    def __init__(self, width: int = 0, height: int = 0, title: str = "Game Window", icon: str = None,
                 flags: Union[list[int], int] = 0,
                 depth: int = 0, display: int = 0, vsync: bool = False):
        Input.update()
        self.running = True
        totalFlags = 0
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

            for drawable in arrays.drawables:
                drawable.update(self.screen)
                if not drawable.persistent:
                    arrays.drawables.remove(drawable)

            Input.update()
            pygame.display.flip()
            RealTime.tick()

    def quit(self):
        self.running = False
        pygame.quit()
