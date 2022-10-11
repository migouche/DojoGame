import pygame.draw

from dojogame.dojographics import arrays
from dojogame.dojomaths.transform import *
from dojogame.dojographics.colors import *


class Object:  # TODO: Rework to convert to GameObject child
    def __init__(self, img, scale):
        # self.transform = transform
        self.transform = Transform(Vector2.zero(), 0, scale)
        self.transform.object = self
        self.Img = pygame.transform.scale(pygame.image.load(img), (self.transform.scale.x, self.transform.scale.y))
        self.rect = self.Img.get_rect()
        self.offset = scale / 2
        arrays.objects.append(self)

    @classmethod
    def regular_polygon(cls, scale):  # have to add sides parameter
        self = cls.__new__(cls)
        self.transform = Transform(Vector2.zero(), 0, scale)
        self.transform.object = self
        self.Img = pygame.Surface((self.transform.scale.x, self.transform.scale.y))
        self.rect = pygame.draw.lines(self.Img, (255, 255, 255), True, [(0, 0), (1, 0), (1, 1), (0, 1)])

        return self


class GameObject:
    def __init__(self):
        self.collider = None
        self.rigidbody = None
        self.transform = Transform()    

    def draw(self, screen: pygame.Surface) -> pygame.Rect:
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def get_collider(self):
        if self.collider is None:
            raise AttributeError(f"GameObject has no collider")
        else:
            return self.collider

    def get_rigidbody(self):
        if self.rigidbody is None:
            raise AttributeError(f"GameObject has no rigidbody")
        else:
            return self.rigidbody


class Polygon(GameObject):
    def __init__(self, vertices: list, color: Color = Colors.black, width: int = 0, antialias: bool = False):
        super().__init__()
        self._collider = None
        self.local_vertices_positions = vertices
        self.color = color
        self.width = width
        self.antialias = antialias
        self.rect = pygame.Rect(0, 0, 0, 0)
        arrays.game_objects.append(self)

    def get_absolute_vertices_positions(self) -> [Vector2]:
        return [self.transform.relative_pos_to_absolute(v) for v in self.local_vertices_positions]

    def draw(self, screen: pygame.Surface) -> pygame.Rect:
        return pygame.draw.polygon(screen, self.color.to_tuple(),
                                   [v.to_tuple() for v in self.get_absolute_vertices_positions()], self.width)

    def update(self, screen: pygame.Surface = None):
        try:
            self.get_collider().aabb.update_aabb()  # change later to get_collider().update()
        except AttributeError:
            pass

        if screen is not None:
            self.rect = self.draw(screen)

    @staticmethod
    def Rectangle(width: int, height: int, color: Color = Colors.black, line_width: int = 0,
                  antialias: bool = False) -> 'Polygon':
        vertices = [Vector2(-width / 2, -height / 2), Vector2(width / 2, -height / 2),
                    Vector2(width / 2, height / 2), Vector2(-width / 2, height / 2)]
        return Polygon(vertices, color, line_width, antialias)

    @staticmethod
    def Square(size: int, color: Color = Colors.black, line_width: int = 0,
               antialias: bool = False) -> 'Polygon':
        return Polygon.Rectangle(size, size, color, line_width, antialias)


class Circle(GameObject):
    def __init__(self, radius: float, color: Color = Colors.black, width: int = 0):
        super().__init__()
        self.radius = radius
        self.color = color
        self.width = width
        self.rect = pygame.Rect(0, 0, 0, 0)
        arrays.game_objects.append(self)

    def draw(self, screen: pygame.Surface) -> pygame.Rect:
        return pygame.draw.circle(screen, self.color.to_tuple(),
                                  self.transform.position.to_tuple(), self.radius, self.width)

    def update(self, screen: pygame.Surface = None):
        try:
            self.get_collider().aabb.update_aabb()  # change later to get_collider().update()
        except AttributeError:
            pass

        if screen is not None:
            self.rect = self.draw(screen)


class Text:  # TODO: Rework to convert to GameObject child
    def __init__(self, font, size: int, txtColor: Color = Colors.black, bgColor: Color = Colors.white):
        self.rectTransform = RectTransform(Vector2.zero(), 0)
        self.rectTransform.text = self
        self.text = ""
        self.size = size
        self.font = font
        self.textColor = txtColor
        self.BGColor = bgColor
        self.renderFont = pygame.font.Font(self.font, self.size)
        self.renderText = pygame.Surface.__new__(pygame.Surface)
        self.set_text(self.text)
        self.rect = self.renderText.get_rect()
        self.rect.center = self.rectTransform.position.to_tuple()
        arrays.texts.append(self)

    def set_text(self, text):
        self.text = text
        self.update_text()

    def set_size(self, size):
        self.size = size
        self.update_text()

    def set_textColor(self, color):
        self.textColor = color
        self.update_text()

    def setTextColour(self, color):
        self.textColor = color
        self.update_text()

    def set_bg_color(self, color):
        self.BGColor = color
        self.update_text()

    def set_bg_colour(self, color):
        self.BGColor = color
        self.update_text()

    def update_text(self):
        self.renderFont = pygame.font.Font(self.font, self.size)
        self.renderText = self.renderFont.render(str(self.text), True,
                                                 self.textColor.to_tuple(),
                                                 self.BGColor.to_tuple())
