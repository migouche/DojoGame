import pygame.draw

from dojogame.dojodata import arrays
from dojogame.dojomaths import *
from dojogame.dojomaths.vectors import Vector2
from dojogame.dojographics.colors import *


class GameObject:
    def __init__(self, position: Vector2 = Vector2.zero(), rotation: float = 0,
                 scale: Vector2 = Vector2(1, 1), parent: Transform = None):
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.collider = None
        self.rigidbody = None
        self.transform = Transform(position, rotation, scale, game_object=self, parent=parent)
        arrays.game_objects.append(self)

    def draw(self, screen: pygame.Surface) -> pygame.Rect:
        raise NotImplementedError

    def update(self, screen):
        self.transform.update()
        try:
            self.get_collider().aabb.update_aabb()  # TODO: change later to get_collider().update()
        except AttributeError:
            pass

        try:
            self.get_rigidbody().update_action()
        except AttributeError:
            pass

        if screen is not None:
            self.rect = self.draw(screen)

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

    @staticmethod
    def get_rotated_surface_size(surface: pygame.Surface, rotation: float) -> Vector2Int:
        return (Vector2.from_tuple(pygame.transform.rotate(surface, rotation).
                                   get_size()) / 2).to_vector2_int()


class Sprite(GameObject):
    def __init__(self, img: str, scale: Vector2, position: Vector2 = Vector2.zero(),
                 rotation: float = 0, parent=None):
        super().__init__(position, rotation, scale, parent)
        self.transform.set_local_scale(scale)
        self._scale = scale
        # self.transform = transform
        self.Img = pygame.transform.scale(pygame.image.load(img), self.transform.scale.to_tuple())
        self.img_rect = self.Img.get_rect()
        self.offset = scale / 2
        arrays.objects.append(self)

    def draw(self, screen) -> pygame.Rect:
        if self._scale != self.transform.scale:  # to avoid scaling the image every frame
            self._scale = self.transform.scale
            self.Img = pygame.transform.scale(self.Img, self.transform.scale.to_tuple())
            self.img_rect = self.Img.get_rect()

        return screen.blit(pygame.transform.rotate(self.Img, -self.transform.rotation),
                           (self.transform.position.to_vector2_int() -
                            GameObject.get_rotated_surface_size(self.Img,
                                                                self.transform.rotation)).
                           to_tuple())


class Polygon(GameObject):
    def __init__(self, vertices: list, color: Color = Colors.black,
                 width: int = 0, antialias: bool = False):
        super().__init__()
        self._collider = None
        self.local_vertices_positions = vertices
        self.color = color
        self.width = width
        self.antialias = antialias
        # arrays.game_objects.append(self)

    def get_absolute_vertices_positions(self) -> [Vector2]:
        return [self.transform.relative_pos_to_absolute(v) for v in
                [Vector2.scale(lv, self.transform.scale) for lv in self.local_vertices_positions]]

    def draw(self, screen: pygame.Surface) -> pygame.Rect:
        return pygame.draw.polygon(screen, self.color.to_tuple(),
                                   [v.to_tuple() for v in self.get_absolute_vertices_positions()],
                                   self.width)

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
        # arrays.game_objects.append(self)

    def draw(self, screen: pygame.Surface) -> pygame.Rect:
        return pygame.draw.circle(screen, self.color.to_tuple(),
                                  self.transform.position.to_tuple(), self.radius, self.width)


class Text(GameObject):
    def __init__(self, font, size: int, txt_color: Color = Colors.black,
                 bg_color: Color = Colors.white):
        super().__init__()
        self.text = ""
        self.size = size
        self.font = font
        self.text_color = txt_color
        self.bg_color = bg_color
        self.render_font = pygame.font.Font(self.font, self.size)
        self.render_text = pygame.Surface.__new__(pygame.Surface)
        self.set_text(self.text)
        self.rect = self.render_text.get_rect()
        self.rect.center = self.transform.position.to_tuple()
        arrays.texts.append(self)

    def set_text(self, text):
        self.text = text
        self.update_text()

    def set_size(self, size):
        self.size = size
        self.update_text()

    def set_textColor(self, color):
        self.text_color = color
        self.update_text()

    def setTextColour(self, color):
        self.text_color = color
        self.update_text()

    def set_bg_color(self, color):
        self.bg_color = color
        self.update_text()

    def set_bg_colour(self, color):
        self.bg_color = color
        self.update_text()

    def update_text(self):
        self.render_font = pygame.font.Font(self.font, self.size)
        self.render_text = self.render_font.render(str(self.text), True,
                                                   self.text_color.to_tuple(),
                                                   self.bg_color.to_tuple())

    def draw(self, screen: pygame.Surface) -> pygame.Rect:
        self.update_text()

        return screen.blit(pygame.transform.rotate(self.render_text, -self.transform.rotation),
                           (self.transform.position.to_vector2_int() -
                            GameObject.get_rotated_surface_size(self.render_text,
                                                                self.transform.rotation)).
                           to_tuple())
