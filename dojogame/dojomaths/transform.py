from dojogame.dojomaths.vectors import *
from dojogame.dojodata.enums import *

import pygame.transform
from typing import Union


class Transform:
    def __init__(self, pos: Vector2 = Vector2.zero(), angle: float = 0, scale: Vector2 = Vector2(1, 1),
                 space: Space = Space.Self, game_object: Union['GameObject', 'Object'] = None, parent: 'Transform' = None):
        self.parent = parent
        self.rotation = angle
        self.scale = scale
        self.game_object = game_object

        if space == Space.Self:
            self.local_position = pos
        elif space == Space.World:
            self.position = pos
        else:
            raise TypeError("Wrong Space given")

        self.update()

    def set_pos(self, pos, space: Space = Space.Self):
        self.position = pos

    def translate(self, translation, space: Space = Space.Self):
        self.position += translation

    def set_scale(self, scale):
        self.scale = scale
        self.update()

    def set_rot(self, angle, space: Space = Space.Self):
        self.rotation = angle % 360

    def rotate(self, angle):
        self.rotation = (self.rotation + angle) % 360

    def rotate_around_origin(self, angle: float, origin: Vector2):
        s = math.sin(angle * Mathf.Deg2Rad)
        c = math.cos(angle * Mathf.Deg2Rad)

        point = self.position - origin

        self.position = Vector2(point.x * c - point.y * s + origin.x, point.x * s + point.y * c + origin.y)

    def relative_pos_to_absolute(self, pos: Vector2) -> Vector2:
        t = Transform(pos + self.position)
        t.rotate_around_origin(self.rotation, self.position)
        return t.position

    def absolute_pos_to_relative(self, pos: Vector2) -> Vector2:
        t = Transform(pos - self.position)
        t.rotate_around_origin(-self.rotation, self.position)
        return t.position

    def update_position(self):
        if self.parent is None:
            self.position = self.local_position
        else:
            self.position = self.parent.relative_pos_to_absolute(self.local_position)

    def update(self):  # TODO: Change?
        self.update_position()
        try:
            self.object.offset = self.scale / 2
            self.object.Img = pygame.transform.scale(self.object.Img,
                                                     (self.scale.x,
                                                      self.scale.y))
            self.object.Img.get_rect()
        except AttributeError:
            pass


class RectTransform:
    def __init__(self, pos, angle):
        self.position = pos
        self.rotation = angle
        self.text = None

    def set_pos(self, pos):
        self.position = pos
        self.text.rect.center = (self.position.x, self.position.y)

    def translate(self, translation):
        self.set_pos(self.position + translation)

    def set_rot(self, angle):
        self.rotation = angle % 360

    def rotate(self, angle):
        self.rotation = (self.rotation + angle) % 360
