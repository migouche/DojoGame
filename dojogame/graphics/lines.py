from dojogame.maths.vectors import Vector2
from dojogame.graphics.colors import Color, Colors
from dojogame.graphics.drawable import Drawable
from typing import Callable

import pygame.draw


class Lines(Drawable):
    def __init__(self, func: Callable):
        self.draw = func
        super().__init__(False)

    def draw(self, screen: 'pygame.Surface') -> 'pygame.Rect':
        pass

    @staticmethod
    def draw_line(_from: Vector2, _to: Vector2,
                  width: int = 1, color: Color = Colors.black) -> 'Lines':
        return Lines(lambda screen: pygame.draw.line(
            screen, color.to_tuple(), _from.to_tuple(), _to.to_tuple(), width))

    @staticmethod
    def draw_ray(start: Vector2, _dir: float | Vector2,
                 length: int, width: int = 1, color: Color = Colors.black) -> 'Lines':
        vec = _dir.normalized() * length if type(_dir) is Vector2 else Vector2.from_angle_deg(
            _dir).normalized() * length
        return Lines.draw_line(start, start + vec, width, color)

    @staticmethod
    def draw_polygon(points: list[Vector2], width: int = 1, color: Color = Colors.black) -> 'Lines':
        if len(points) < 3:
            raise ValueError("points must have at least 3 elements")
        return Lines(lambda screen:
                     pygame.draw.polygon(screen, color.to_tuple(),
                                         [point.to_tuple() for point in points], width))

    @staticmethod
    def draw_axis_aligned_bounding_box(col: 'Collider', color: Color = Colors.black,
                                       width: int = 1) -> 'Lines':
        if col is None:
            raise ValueError("Collider is None")

        aabb = col.aabb

        return Lines.draw_rectangle([aabb.min_v,
                                     Vector2(aabb.min_v.x, aabb.max_v.y),
                                     aabb.max_v,
                                     Vector2(aabb.max_v.x, aabb.min_v.y)], color, width)

    @staticmethod
    def draw_rectangle(vertices: list[Vector2, Vector2, Vector2, Vector2],
                       color: Color = Colors.black, width: int = 1) -> 'Lines':
        if len(vertices) != 4:
            raise ValueError("Vertices must be 4")
        return Lines.draw_polygon(vertices, width, color)

    @staticmethod
    def draw_circle(position: Vector2, radius: int,
                    color: Color = Colors.black, width: int = 1) -> 'Lines':
        return Lines(lambda screen: pygame.draw.circle(
            screen, color.to_tuple(), position.to_tuple(), radius, width))
