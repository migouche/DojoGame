from dojogame.dojophysics.collisions import CircleCollider, PolygonCollider
from dojogame.dojomaths.vectors import Vector2
from dojogame.dojomaths.dojomathfunctions import Mathf
import math


class RaycastHit:
    def __init__(self, collide: bool, point: Vector2 = None, normal: Vector2 = None, dist: float = None, collider=None):
        self.collide = collide
        self.point = point
        self.normal = normal
        self.distance = dist
        self.collider = collider

    def __bool__(self):
        return self.collide


class Raycast:
    @staticmethod
    def raycast(start: Vector2, _dir: Vector2) -> RaycastHit:
        pass

    @staticmethod
    def raycast_circle(start: Vector2, _dir: Vector2, circle_collider: CircleCollider) -> RaycastHit:
        if circle_collider is None:
            raise ValueError("circle collider is None. Did you forget to add a collider to the object?")

        circle = circle_collider.circle

        r_squared = circle.radius ** 2
        direction = _dir.normalized()

        origin_to_circle = circle.transform.position - start
        origin_to_circle_squared = origin_to_circle.x ** 2 + origin_to_circle.y ** 2

        a = Vector2.dot(origin_to_circle, direction)
        b_squared = origin_to_circle_squared - a ** 2

        if r_squared - b_squared < 0:
            return RaycastHit(False)

        f = math.sqrt(r_squared - b_squared)

        if origin_to_circle_squared < r_squared:  # inside circle
            t = a + f
        else:
            t = a - f

        if t < 0:
            return RaycastHit(False)

        point = start + direction * t
        normal = (point - circle.transform.position).normalized()

        return RaycastHit(True, point, normal, t, circle)

    @staticmethod
    def raycast_segment(start: Vector2, _dir: Vector2,
                        point0: Vector2, point1: Vector2, distance: float | int) -> RaycastHit:
        seg = point1 - point0
        seg_perp = seg.left_perpendicular()
        perp_dot_dir = Vector2.dot(_dir, seg_perp)

        if perp_dot_dir == 0 or perp_dot_dir == Mathf.epsilon or -perp_dot_dir == Mathf.epsilon:
            return RaycastHit(False)

        d = point0 - start

        t = Vector2.dot(seg_perp, d) / perp_dot_dir
        s = Vector2.dot(_dir.left_perpendicular(), d) / perp_dot_dir

        if 0 <= t <= distance and 0 <= s <= 1:
            return RaycastHit(True, start + _dir * t, seg_perp.normalized(), t)
        return RaycastHit(False)

    @staticmethod
    def raycast_polygon(start: Vector2, _dir: Vector2,
                        polygon_collider: PolygonCollider, distance) -> RaycastHit:
        if polygon_collider is None:
            raise ValueError("polygon collider is None. Did you forget to add a collider to the object?")

        polygon = polygon_collider.polygon
        vertices = polygon.get_absolute_vertices_positions()

        t = float("inf")
        crossings = 0

        point = normal = Vector2.zero()

        for i in range(len(vertices)):
            j = (i + 1) % len(vertices)

            if hit := Raycast.raycast_segment(start, _dir, vertices[i], vertices[j], float("inf")):
                crossings += 1
                if hit.distance < t and distance <= distance:
                    t = hit.distance
                    normal = hit.normal
                    point = hit.point
        if crossings > 0 and crossings % 2 == 0:
            return RaycastHit(True, point, normal, t)
        return RaycastHit(False)
