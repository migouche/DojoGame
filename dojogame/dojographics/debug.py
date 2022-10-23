from dojogame.dojomaths.vectors import Vector2
from dojogame.dojographics.colors import Color, Colors
from dojogame.dojodata import arrays
import pygame.draw


class Debug:
    @staticmethod
    def draw_axis_aligned_bounding_box(col: 'Collider', color: Color = Colors.black, width: int = 1):
        if col is None:
            raise ValueError("Collider is None")

        aabb = col.aabb

        Debug.draw_rectangle_vertices([aabb.min_v,
                                       Vector2(aabb.min_v.x, aabb.max_v.y),
                                       aabb.max_v,
                                       Vector2(aabb.max_v.x, aabb.min_v.y)], color, width)

    @staticmethod
    def draw_rectangle_vertices(vertices: list[Vector2, Vector2, Vector2, Vector2],
                                color: Color = Colors.black, width: int = 1):
        if len(vertices) != 4:
            raise ValueError("Vertices must be 4")
        arrays.debug.append(lambda screen: pygame.draw.polygon(screen, color.to_tuple(),
                                                        [v.to_tuple() for v in vertices], width))

    @staticmethod
    def draw_circle(position: Vector2, radius: int, color: Color = Colors.black, width: int = 1):
        arrays.debug.append(lambda screen: pygame.draw.circle(screen, color.to_tuple(), position.to_tuple(), radius, width))


class Lines:
    @staticmethod
    def draw_line(_from: Vector2, _to: Vector2, width: int = 1, color: Color = Colors.black):
        arrays.debug.append(
            lambda screen: pygame.draw.line(screen, color.to_tuple(), _from.to_tuple(), _to.to_tuple(), width))

    @staticmethod
    def draw_ray(start: Vector2, _dir: float | Vector2, length: int, width: int = 1, color: Color = Colors.black):
        vec = _dir.normalized() * length if type(_dir) is Vector2 else Vector2.from_angle_deg(
            _dir).normalized() * length
        Lines.draw_line(start, start + vec, width, color)