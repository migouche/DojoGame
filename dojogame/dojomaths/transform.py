import math

from dojogame.dojomaths.vectors import Vector2
from dojogame.dojomaths.matrix import Matrix
from dojogame.dojomaths.dojomathfunctions import Mathf
from dojogame.dojodata.enums import Space

import pygame.transform


class Transform:
    def __init__(self, pos: Vector2 = Vector2.zero(), angle: float = 0, scale: Vector2 = Vector2(1, 1),
                 space: Space = Space.Self, game_object: 'GameObject' = None,
                 parent: 'Transform' = None):
        self.children = []
        self.parent = parent
        self.set_parent(parent)
        self.local_scale = scale
        self.game_object = game_object

        self.local_position = self.position = Vector2.zero()
        self.local_rotation = self.rotation = 0

        self.local_translation_matrix = self.\
            local_rotation_matrix = self.\
            local_scale_matrix = Matrix.empty(2, 2)

        self.set_position(pos, space)
        self.set_rotation(angle, space)

        self.last_position_space = self.last_rotation_space = space

        self.update()

    def set_position(self, pos, space: Space = Space.Self):
        if space == Space.Self:
            self.local_position = pos
        elif space == Space.World:
            raise NotImplementedError
        else:
            raise TypeError("Wrong Space given")

    def translate(self, translation, space: Space = Space.Self):
        self.set_position(self.get_position(space) + translation, space)

    def get_position(self, space: Space = Space.Self):
        if space == Space.Self:
            return self.local_position
        elif space == Space.World:
            return self.position
        else:
            raise TypeError("Wrong Space given")

    def set_local_scale(self, scale):
        self.local_scale = scale
        # self.update()

    def get_rotation(self, space: Space = Space.Self):
        if space == Space.Self:
            return self.local_rotation
        elif space == Space.World:
            return self.rotation
        else:
            raise TypeError("Wrong Space given")

    def set_rotation(self, angle, space: Space = Space.Self):
        if space == Space.Self:
            self.local_rotation = angle % 360
        elif space == Space.World:
            raise NotImplementedError
        else:
            raise TypeError("Wrong Space given")

    def rotate(self, angle, space: Space = Space.Self):
        self.set_rotation(angle + self.get_rotation(space), space)

    def rotate_around_origin(self, angle: float, origin: Vector2):
        s = math.sin(angle * Mathf.Deg2Rad)
        c = math.cos(angle * Mathf.Deg2Rad)

        point = self.position - origin

        self.position = Vector2(point.x * c - point.y * s + origin.x,
                                point.x * s + point.y * c + origin.y)

    def relative_pos_to_absolute(self, pos: Vector2) -> Vector2:
        t = Transform(pos + self.get_position(Space.World))
        t.rotate_around_origin(self.rotation, self.position)
        return t.position

    def absolute_pos_to_relative(self, pos: Vector2) -> Vector2:
        t = Transform(self.get_position(Space.World) - pos)
        t.rotate_around_origin(-self.rotation, self.position)
        return pos - t.position

    def set_parent(self, parent: 'Transform'):
        self.parent = parent
        try:
            self.parent.children.append(self)
        except AttributeError:
            pass

    def get_parent(self):
        return self.parent

    def get_child(self, i: int):
        return self.children[i]

    def update_position(self):
        self.local_translation_matrix = self.local_position.to_matrix_column()
        self.local_rotation_matrix = \
            Matrix([[c := math.cos(self.local_rotation * Mathf.Deg2Rad),
                     -(s := math.sin(self.local_rotation * Mathf.Deg2Rad))],
                    [s, c]])
        self.local_scale_matrix = Matrix([[self.local_scale.x, 0], [0, self.local_scale.y]])

        if self.parent is not None:
            self.position = Vector2.from_matrix(self.parent.local_translation_matrix +
                                                (self.parent.local_rotation_matrix *
                                                 (self.parent.local_scale_matrix *
                                                  self.local_position.to_matrix_column())))
            self.rotation = self.parent.rotation + self.local_rotation
        else:
            self.position = self.local_position
            self.rotation = self.local_rotation

    def update(self):  # TODO: Change?
        self.update_position()
        try:
            self.game_object.offset = self.local_scale / 2
            self.game_object.Img = pygame.transform.scale(self.game_object.Img,
                                                          (self.local_scale.x,
                                                           self.local_scale.y))
            self.game_object.Img.get_rect()
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
