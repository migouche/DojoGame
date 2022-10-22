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

    def get_collider(self) -> 'Collider':
        if self.collider is None:
            raise AttributeError(f"GameObject has no collider")
        else:
            return self.collider

    def get_rigidbody(self) -> 'Rigidbody':
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
        self.image_path = img
        self.image = pygame.image.load(img)
        self.image_rect = self.image.get_rect()
        self.update_image()
        self.offset = scale / 2
        arrays.objects.append(self)

    def update_image(self):
        self.image = pygame.transform.scale(pygame.image.load(self.image_path),
                                            self.transform.local_scale.to_tuple())
        self.image_rect = self.image.get_rect()

    def draw(self, screen) -> pygame.Rect:
        if self._scale != self.transform.local_scale:  # to avoid scaling the image every frame
            self._scale = self.transform.local_scale
            self.update_image()

        return screen.blit(pygame.transform.rotate(self.image, -self.transform.rotation),
                           (self.transform.position.to_vector2_int() -
                            GameObject.get_rotated_surface_size(self.image,
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
        return [self.transform.relative_pos_to_absolute(v)
                for v in [Vector2.scale(lv, self.transform.local_scale)
                          for lv in self.local_vertices_positions]]

    def draw(self, screen: pygame.Surface) -> pygame.Rect:
        points = [v.to_tuple() for v in self.get_absolute_vertices_positions()]
        lx, ly = zip(*points)
        min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
        target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
        shape_surface = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        pygame.draw.polygon(shape_surface, self.color.to_tuple(),
                            [(x - min_x, y - min_y) for x, y in points])

        return screen.blit(shape_surface, target_rect)

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
    def __init__(self, font, size: int, txt_color: Color = Colors.black, ):
        super().__init__()
        self.text = ""
        self.size = size
        self.font = font
        self.text_color = txt_color
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

    def set_text_color(self, color):
        self.text_color = color
        self.update_text()

    def set_text_colour(self, color):
        self.text_color = color
        self.update_text()

    def update_text(self):
        self.render_font = pygame.font.Font(self.font, self.size)
        self.render_text = self.render_font.render(str(self.text), True,
                                                   self.text_color.to_tuple())
        self.render_text.set_alpha(self.text_color.alpha)

    def draw(self, screen: pygame.Surface) -> pygame.Rect:
        self.update_text()

        return screen.blit(pygame.transform.rotate(self.render_text, -self.transform.rotation),
                           (self.transform.position.to_vector2_int() -
                            GameObject.get_rotated_surface_size(self.render_text,
                                                                self.transform.rotation)).
                           to_tuple())
