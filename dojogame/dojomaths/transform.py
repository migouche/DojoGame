from dojogame.dojomaths.vectors import *
import pygame.transform

class Transform:
    def __init__(self, pos: Vector2 = Vector2.zero(), angle: float = 0, scale: Vector2 = Vector2(1, 1)):
        self.position = pos
        self.rotation = angle
        self.scale = scale
        self.object = None

    def set_pos(self, pos):
        self.position = pos

    def translate(self, translation):
        self.position += translation

    def set_scale(self, scale):
        self.scale = scale
        self.update()

    def set_rot(self, angle):
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

    def update(self):
        self.object.offset = self.scale / 2
        self.object.Img = pygame.transform.scale(self.object.Img,
                                                 (self.scale.x,
                                                  self.scale.y))
        self.object.Img.get_rect()

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