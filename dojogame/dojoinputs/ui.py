from dojogame.dojographics.gameobjects import GameObject
from dojogame.dojomaths.transform import Transform
from dojogame.dojomaths.vectors import Vector2
from dojogame.dojoinputs.inputs import Input

from typing import Callable


class Button(GameObject):
    def __init__(self, background: GameObject, foreground: GameObject = None):
        super().__init__()
        self.transform = Transform(game_object=self)
        self.background = background
        self.foreground = foreground

        self.background.transform.set_parent(self.transform)
        self.background.transform.set_position(Vector2.zero())

        self.old_hovered = self.hovered = False
        self.old_clicked = self.clicked = False

        if self.foreground is not None:
            self.foreground.transform.set_parent(self.background.transform)
            self.foreground.transform.set_position(Vector2.zero())

        self._on_click = self._on_hover_enter = self._on_hover_stay = \
            self._on_hover_exit = self._on_hold = self._on_release = lambda: None

    def calculate_mouse(self):
        self.old_clicked = self.clicked
        self.old_hovered = self.hovered
        self.hovered = self.background.collider. \
            point_inside_collider(Input.get_mouse_position())

        if self.hovered:
            if Input.get_mouse_button_down(1):
                self.clicked = True
            elif Input.get_mouse_button_up(1):
                self.clicked = False
        else:
            self.clicked = False

        if self.hovered and not self.old_hovered:
            self._on_hover_enter()
        elif self.hovered and self.old_hovered:
            self._on_hover_stay()
        elif not self.hovered and self.old_hovered:
            self._on_hover_exit()

        if self.clicked and not self.old_clicked:
            self._on_click()
        elif self.clicked and self.old_clicked:
            self._on_hold()
        elif not self.clicked and self.old_clicked:
            self._on_release()

    def draw(self, screen):  # TODO: add update function to GameObject children
        self.calculate_mouse()
        self.background.draw(screen)
        if self.foreground is not None:
            self.foreground.draw(screen)

    def on_click(self, func: Callable):  # decorator
        self._on_click = func

    def on_hold(self, func: Callable):  # decorator
        self._on_hold = func

    def on_release(self, func: Callable):  # decorator
        self._on_release = func

    def on_hover_enter(self, func: Callable):  # decorator
        self._on_hover_enter = func

    def on_hover_stay(self, func: Callable):  # decorator
        self._on_hover_stay = func

    def on_hover_exit(self, func: Callable):  # decorator
        self._on_hover_exit = func
