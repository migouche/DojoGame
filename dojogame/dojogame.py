import math
import random
import sys
import time
from enum import Enum
from typing import Union

import pygame
from pygame.constants import *

sys.path.append("")

from dojogame.vectors import *
from dojogame.dojomathfunctions import *


class Quaternion:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    @staticmethod
    def euler_angles_rad(x, y, z):
        return Quaternion(
            math.sin(x / 2) * math.cos(y / 2) * math.cos(z / 2) - math.cos(x / 2) * math.sin(y / 2) * math.sin(z / 2),
            math.cos(x / 2) * math.sin(y / 2) * math.cos(z / 2) + math.sin(x / 2) * math.cos(y / 2) * math.sin(z / 2),
            math.cos(x / 2) * math.cos(y / 2) * math.sin(z / 2) - math.sin(x / 2) * math.sin(y / 2) * math.cos(z / 2),
            math.cos(x / 2) * math.cos(y / 2) * math.cos(z / 2) + math.sin(x / 2) * math.sin(y / 2) * math.sin(z / 2))

    @staticmethod
    def euler_angles_deg(x, y, z):
        return Quaternion.euler_angles_rad(x * Mathf.Deg2Rad, y * Mathf.Deg2Rad, z * Mathf.Deg2Rad)


objects = []
texts = []
debug = []
game_objects = []
polygon_colliders = []
lambdas = {}
IDCounter = 1


class Color:
    def __init__(self, r: int, g: int, b: int, a: int = 255):
        self.red = r
        self.green = g
        self.blue = b
        self.alpha = a

    def __eq__(self, c):
        return self.red == c.red and self.green == c.green and self.blue == c.blue and self.alpha == c.alpha

    @staticmethod
    def from_hex(h):
        c = tuple(int(h.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
        return Color(c[0], c[1], c[2])

    def to_tuple(self):
        return self.red, self.green, self.blue, self.alpha


class Colors:
    white = Color(255, 255, 255)
    black = Color(0, 0, 0)
    red = Color(255, 0, 0)
    green = Color(0, 255, 0)
    blue = Color(0, 0, 255)
    purple = Color(100, 0, 255)
    transparent = Color(0, 0, 0, 0)


Colour = Color
Colours = Colors


class Object:
    def __init__(self, img, scale):
        # self.transform = transform
        self.transform = Transform(Vector2.zero(), 0, scale)
        self.transform.object = self
        self.Img = pygame.transform.scale(pygame.image.load(img), (self.transform.scale.x, self.transform.scale.y))
        self.rect = self.Img.get_rect()
        self.offset = scale / 2
        objects.append(self)

    @classmethod
    def regular_polygon(cls, scale):  # have to add sides parameter
        self = cls.__new__(cls)
        self.transform = Transform(Vector2.zero(), 0, scale)
        self.transform.object = self
        self.Img = pygame.Surface((self.transform.scale.x, self.transform.scale.y))
        self.rect = pygame.draw.lines(self.Img, (255, 255, 255), True, [(0, 0), (1, 0), (1, 1), (0, 1)])

        return self


class ForceMode(Enum):
    Force = 1
    Acceleration = 2
    Impulse = 3
    VelocityChange = 4


class Space(Enum):
    World = 1
    Self = 2


class Action:
    def __init__(self, dSpeed: Vector2 = Vector2.zero(), dAngle: float = 0):
        self.dSpeed = dSpeed
        self.dAngle = dAngle

    def __add__(self, other):
        return Action(self.dSpeed + other.dSpeed, self.dAngle + other.dAngle)


class Rigidbody:
    def __init__(self, mass: float):
        self.totalAction = Action()
        # self.position = pos
        # self.angle = angle
        self.velocity = Vector2.zero()
        self.angularVelocity = 0
        self.mass = mass
        self.kinematic = False
        self.useGravity = False  # May use it later, may not

    def add_force_at_position(self, force: Vector2, position: Vector2,
                              mode: ForceMode = ForceMode.Force,
                              space: Space = Space.World):

        # posRel = position if space == Space.Self else \
        #    position - self.object.transform.position if space == Space.World else None
        if space == Space.Self:
            absolute_pos = self.object.transform.relative_pos_to_absolute(position)
            absolute_force = Vector2.rotate_by_degs(force, self.object.transform.rotation)

            self.add_force_at_position(absolute_force, absolute_pos, mode, Space.World)
            return
        pos_rel = position - self.object.transform.position if space == Space.World else None
        if pos_rel is None:
            raise TypeError("Wrong Space given")

        if mode == ForceMode.Force:  # dv = F * dt / m
            self.totalAction += Action(f := force * RealTime.delta_time / self.mass, Vector2.cross(pos_rel, f))
        elif mode == ForceMode.Acceleration:  # dv = F * dt
            self.totalAction += Action(f := force * RealTime.delta_time, Vector2.cross(pos_rel, f))
        elif mode == ForceMode.Impulse:  # dv = F / m
            self.totalAction += Action(f := force / self.mass, Vector2.cross(pos_rel, f))
        elif mode == ForceMode.VelocityChange:  # dv = F
            self.totalAction += Action(f := force, Vector2.cross(pos_rel, f))
        else:
            raise TypeError("Wrong ForceMode given")

    def add_force(self, force: Vector2, mode: ForceMode = ForceMode.Force):
        self.add_force_at_position(force, self.object.transform.position, mode)

    def update_action(self):
        self.velocity += self.totalAction.dSpeed
        self.angularVelocity += self.totalAction.dAngle

        self.object.transform.position += self.velocity * RealTime.delta_time
        self.object.transform.rotation += self.angularVelocity * RealTime.delta_time

        self.totalAction = Action()


class GameObject:
    def draw(self, screen: pygame.Surface) -> pygame.Rect:
        raise NotImplementedError

    def update(self):
        raise NotImplementedError


class Polygon(GameObject):
    def __init__(self, vertices: list, color: Color, width: int = 0, antialias: bool = False,
                 rigidbody: bool = False, mass: int = 1):
        self.local_vertices_positions = vertices
        self.transform = Transform()
        self.color = color
        self.width = width
        self.antialias = antialias
        self.collider = PolygonCollider(self)
        self.rect = pygame.Rect(0, 0, 0, 0)
        game_objects.append(self)

    def get_absolute_vertices_positions(self) -> [Vector2]:
        return [self.transform.relative_pos_to_absolute(v) for v in self.local_vertices_positions]

    def draw(self, screen: pygame.Surface) -> pygame.Rect:
        return pygame.draw.polygon(screen, self.color.to_tuple(),
                                   [v.to_tuple() for v in self.get_absolute_vertices_positions()], self.width)

    def update(self, screen: pygame.Surface = None):
        self.collider.aabb.update_aabb()
        if screen is not None:
            self.rect = self.draw(screen)


class Circle(GameObject):
    def __init__(self, radius: float, color: Color = Colors.black, width: int = 0,
                 rigidbody: bool = False, mass: int = 1):
        self.radius = radius
        self.transform = Transform()
        self.color = color
        self.width = width
        self.collider = CircleCollider(self)
        self.rect = pygame.Rect(0, 0, 0, 0)
        game_objects.append(self)

    def draw(self, screen: pygame.Surface) -> pygame.Rect:
        return pygame.draw.circle(screen, self.color.to_tuple(),
                                  self.transform.position.to_tuple(), self.radius, self.width)

    def update(self, screen: pygame.Surface = None):
        self.collider.aabb.update_aabb()
        if screen is not None:
            self.rect = self.draw(screen)


class Collision:
    def __init__(self, collide: bool, point: Vector2 = None, normal: Vector2 = None):
        self.collide = collide
        self.point = point
        self.normal = normal

    def __bool__(self):
        return self.collide


class AxisAlignedBoundingBox:
    def __init__(self, obj: Polygon | Circle):
        self.obj = obj
        self.min_v = self.max_v = Vector2.zero()
        self.update_aabb()

    def update_aabb(self):
        if isinstance(self.obj, Polygon):
            vertices = self.obj.get_absolute_vertices_positions()
            max_x = max_y = float("-inf")
            min_x = min_y = float("inf")
            for vertex in vertices:
                if vertex.x > max_x:
                    max_x = vertex.x
                if vertex.y > max_y:
                    max_y = vertex.y
                if vertex.x < min_x:
                    min_x = vertex.x
                if vertex.y < min_y:
                    min_y = vertex.y
            self.min_v = Vector2(min_x, min_y)
            self.max_v = Vector2(max_x, max_y)
        elif isinstance(self.obj, Circle):
            self.min_v = self.obj.transform.position - Vector2(self.obj.radius, self.obj.radius)
            self.max_v = self.obj.transform.position + Vector2(self.obj.radius, self.obj.radius)
        else:
            raise TypeError("Wrong type of object given")

    def aabb_overlap(self, other: 'AxisAlignedBoundingBox') -> bool:
        return self.min_v.x < other.max_v.x and self.max_v.x > other.min_v.x and \
               self.min_v.y < other.max_v.y and self.max_v.y > other.min_v.y


AABB = AxisAlignedBoundingBox


class Collisions:
    @staticmethod
    def intersect_polygons(p1: Polygon, p2: Polygon) -> Collision:
        if not p1.collider.aabb.aabb_overlap(p2.collider.aabb):
            return Collision(False)

        def find_arithmetic_mean(points: list) -> Vector2:
            x = y = 0

            for j in range(len(points)):
                x += points[j].x
                y += points[j].y
            return Vector2(x / len(points), y / len(points))

        vertices_a = p1.get_absolute_vertices_positions()
        vertices_b = p2.get_absolute_vertices_positions()

        normal = Vector2.zero()
        depth = float('inf')

        for i in range(len(vertices_a)):
            va = vertices_a[i]
            vb = vertices_a[(i + 1) % len(vertices_a)]

            edge = vb - va
            axis = Vector2(-edge.y, edge.x)

            (min_a, max_a) = Collisions.project_vertices(vertices_a, axis)
            (min_b, max_b) = Collisions.project_vertices(vertices_b, axis)

            if min_a >= max_b or min_b >= max_a:
                return Collision(False)

            axis_depth = min(max_a - min_b, max_b - min_a)

            if axis_depth < depth:
                depth = axis_depth
                normal = axis

        for i in range(len(vertices_b)):
            va = vertices_b[i]
            vb = vertices_b[(i + 1) % len(vertices_b)]

            edge = vb - va
            axis = Vector2(-edge.y, edge.x)

            (min_a, max_a) = Collisions.project_vertices(vertices_a, axis)
            (min_b, max_b) = Collisions.project_vertices(vertices_b, axis)

            if min_a >= max_b or min_b >= max_a:
                return Collision(False)

            axis_depth = min(max_a - min_b, max_b - min_a)

            if axis_depth < depth:
                depth = axis_depth
                normal = axis

        center_a = find_arithmetic_mean(vertices_a)
        center_b = find_arithmetic_mean(vertices_b)

        direction = center_b - center_a

        if Vector2.dot(direction, normal) < 0:
            normal = -normal
        return Collision(True, normal=normal)

    @staticmethod
    def project_vertices(vertices: list, axis: Vector2) -> tuple:
        _min = Vector2.dot(vertices[0], axis)
        _max = _min
        for v in vertices:
            p = Vector2.dot(v, axis)
            if p < _min:
                _min = p
            elif p > _max:
                _max = p
        return _min, _max


class PolygonCollider:
    def __init__(self, polygon: Polygon):
        self.polygon = polygon
        self.aabb = AABB(polygon)

    def collide_with(self, other) -> bool:
        return bool(Collisions.intersect_polygons(self.polygon, other.polygon))


class CircleCollider:
    def __init__(self, circle: Circle):
        self.circle = circle
        self.aabb = AABB(circle)


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
    def raycast_circle(start: Vector2, _dir: Vector2, circle: Circle | CircleCollider) -> RaycastHit:
        # r_squared = 0
        direction = _dir.normalized()
        if isinstance(circle, Circle):
            r_squared = circle.radius ** 2
        elif isinstance(circle, CircleCollider):
            r_squared = circle.circle.radius ** 2
        else:
            raise TypeError("circle must be of type Circle or CircleCollider")

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
                        polygon: Polygon | PolygonCollider, distance) -> RaycastHit:
        if isinstance(polygon, Polygon):
            vertices = polygon.get_absolute_vertices_positions()
        elif isinstance(polygon, PolygonCollider):
            vertices = polygon.polygon.get_absolute_vertices_positions()
        else:
            raise TypeError("polygon must be of type Polygon or PolygonCollider")

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


class BaseObject:
    def __init__(self, _lambda, mass: float, position: Vector2, rotation: float, collider: type, color: Color,
                 *args, **kwargs):  # args contains parameters to pass to the collider __init__()
        global IDCounter
        self.id = IDCounter
        IDCounter += 1
        for kwarg in kwargs.items():  # kwargs contains all attributes that need to be added to the object
            setattr(self, kwarg[0], kwarg[1])
        self.color = color
        self.rigidbody = Rigidbody(mass)
        self.transform = Transform(position, rotation, Vector2.zero())
        self.rigidbody.object = self
        self.collider = collider(*args)
        self.collider.id = self.id
        lambdas.update({self: _lambda})


class BaseCollider:
    def hit_inside_collider(self, point: Vector2):
        raise NotImplementedError

    def collide_with(self, other):
        raise NotImplementedError

    def on_trigger_enter(self, func):
        pass

    def on_trigger_stay(self, func):
        pass

    def on_trigger_leave(self, func):
        pass

    def on_collision_enter(self, func):
        pass

    def on_collision_stay(self, func):
        pass

    def on_collision_leave(self, func):
        pass


class CircleOld(BaseObject):
    def __init__(self, radius: int, mass: float = 1, outline: int = 0, color: Color = Colors.black,
                 position: Vector2 = Vector2.zero(), rotation: float = 0):
        super().__init__(lambda screen, obj: pygame.draw.circle(screen,
                                                                obj.color.to_tuple(),
                                                                obj.transform.position.to_tuple(),
                                                                obj.radius, obj.outline),
                         mass, position, rotation, CircleCollider, color, self, radius=radius,
                         outline=outline)


class CircleColliderOld(BaseCollider):
    def __init__(self, circle: Circle):
        self.object = circle

    def hit_inside_collider(self, point: Vector2):
        if Vector2.distance(self.object.transform.position, point) <= self.object.radius:
            n = (point - self.object.transform.position).normalized()
            return RaycastHit(True, self.object.transform.position + n * self.object.radius, n,
                              Vector2.distance(self.object.transform.position, point), collider=self)
        else:
            return RaycastHit(False)

    def collide_with(self, other):
        if hasattr(other, "collider"):
            if isinstance(other, Circle):
                if Vector2.distance(self.object.transform.position,
                                    other.transform.position) < self.object.radius + other.radius:
                    normal = (other.transform.position - self.object.transform.position).normalized()
                    return Collision(True, normal * self.object.radius + self.object.transform.position, normal)
                else:
                    return Collision(False)
            elif isinstance(other, Rectangle):
                '''if other.collider.tryReverseCollision(self.circle):
                    return Collision(True)
                else:
                    smallSide = other.width if other.width < other.height else other.height
                    if smallSide + self.circle.radius > Vector2.distance(self.circle.transform.position,
                                                                         other.transform.position):
                        return Collision(True)
                    else:
                        return Collision(False)'''
                raise NotImplementedError("Circle-Rectangle collisions are not implemented yet")

        else:
            raise TypeError("Argument must be a collider")


class Rectangle(BaseObject):
    def __init__(self, w: int, h: int, mass: float = 1, color: Color = Colors.black,
                 position: Vector2 = Vector2.zero(), rotation: float = 0):
        super().__init__(lambda screen, obj: obj.draw(screen), mass, position, rotation,
                         RectangleCollider,
                         color,
                         self, width=w, height=h)

    def draw(self, screen):  # doing this cause of not multi-line lambdas :v
        colorkey = Colors.white if self.color == Colors.black else Colors.black

        initSquare = pygame.Surface((self.width, self.height))
        initSquare.set_colorkey(colorkey.to_tuple())
        initSquare.fill(self.color.to_tuple())

        imgcopy = initSquare.copy()
        imgcopy.set_colorkey(colorkey.to_tuple())
        rect = imgcopy.get_rect()
        rect.center = self.transform.position.to_tuple()
        old_center = rect.center
        rotSquare = pygame.transform.rotate(initSquare, -self.transform.rotation)
        rect = rotSquare.get_rect()
        rect.center = old_center
        screen.blit(rotSquare, rect)

    def get_vertices(self):
        v = [self.transform.position + Vector2(self.width / 2, self.height / 2),
             self.transform.position + Vector2(self.width / 2, -self.height / 2),
             self.transform.position + Vector2(-self.width / 2, self.height / 2),
             self.transform.position + Vector2(-self.width / 2, -self.height / 2)]

        vf = []
        for pos in v:
            t = Transform(pos)
            t.rotate_around_origin(self.transform.rotation, self.transform.position)
            vf.append(t.position)
        return vf


class RectangleCollider(BaseCollider):
    def __init__(self, rectangle: Rectangle):
        self.object = rectangle

    def hit_inside_collider(self, point: Vector2):  # approximation with starting circle

        diagonal = math.sqrt(((self.object.width / 2) ** 2) + ((self.object.height / 2) ** 2))
        if Vector2.distance(self.object.transform.position, point) < diagonal:
            t = Transform(pos=point)

            t.rotate_around_origin(-self.object.transform.rotation, self.object.transform.position)

            p = t.position
            pos = self.object.transform.position

            # rectangle is horizontal: check for sides:

            w = self.object.width
            h = self.object.height

            if (pos.x - w / 2 < p.x < pos.x + w / 2 and
                    pos.y - h / 2 < p.y < pos.y + h / 2):  # we suppose we are in the surface now
                offset = 1  # in pixels. Better if int

                if pos.y - (h / 2 - offset) > p.y:
                    normal = Vector2(0, -1)
                elif pos.y + (h / 2 - offset) < p.y:
                    normal = Vector2(0, 1)
                elif pos.x - (2 / 2 - offset) > p.x:
                    normal = Vector2(-1, 0)
                elif pos.x + (w / 2 - offset) < p.x:
                    normal = Vector2(1, 0)
                else:
                    return RaycastHit(True, point, (point - self.object.transform.position).normalized(),
                                      collider=self)
                vec = Vector2.from_angle_deg(Vector2.angle_deg(Vector2(1, 0), normal) + self.object.transform.rotation)
                return RaycastHit(True, point, vec.normalized(), collider=self)
            return RaycastHit(False)

    def collide_with(self, other: BaseObject):
        if hasattr(other, "collider"):
            vertices = self.object.get_vertices()
            for v in vertices:
                if hit := other.collider.hit_inside_collider(v):
                    return Collision(True, v, hit.normal)
            try:
                return other.collider.try_reverse_collision(self.object)
            except AttributeError:
                return Collision(False)
        else:
            raise TypeError("Argument must be have a 'collider' property of class BaseCollider")

    def try_reverse_collision(self, other):
        print("reverse collision")
        if hasattr(other, "collider"):
            vertices = self.object.get_vertices()
            for v in vertices:
                if hit := other.collider.hit_inside_collider(v):
                    return Collision(True, v, hit.normal)
            return Collision(False)
        else:
            raise TypeError("Argument must be have a 'collider' property of class BaseCollider")


class Square(Rectangle):
    def __init__(self, side: int, mass: float = 1, color: Color = Colors.black):
        super().__init__(side, side, mass, color)


class Lines:
    @staticmethod
    def draw_line(_from: Vector2, _to: Vector2, width: int = 1, color: Color = Colors.black):
        debug.append(lambda screen: pygame.draw.line(screen, color.to_tuple(), _from.to_tuple(), _to.to_tuple(), width))

    @staticmethod
    def draw_ray(start: Vector2, _dir: Union[float, Vector2], length: int, width: int = 1, color: Color = Colors.black):
        vec = _dir.normalized() * length if type(_dir) is Vector2 else Vector2.from_angle_deg(
            _dir).normalized() * length
        Lines.draw_line(start, start + vec, width, color)


class Debug:
    @staticmethod
    def draw_axis_aligned_bounding_box(polygon: Polygon, color: Color = Colors.black, width: int = 1):
        aabb = polygon.collider.aabb

        Debug.draw_rectangle_vertices([aabb.min_v,
                                       Vector2(aabb.min_v.x, aabb.max_v.y),
                                       aabb.max_v,
                                       Vector2(aabb.max_v.x, aabb.min_v.y)], color, width)

    @staticmethod
    def draw_rectangle_vertices(vertices: list[Vector2, Vector2, Vector2, Vector2],
                                color: Color = Colors.black, width: int = 1):
        if len(vertices) != 4:
            raise ValueError("Vertices must be 4")
        debug.append(lambda screen: pygame.draw.polygon(screen, color.to_tuple(),
                                                        [v.to_tuple() for v in vertices], width))

    @staticmethod
    def draw_circle(position: Vector2, radius: int, color: Color = Colors.black, width: int = 1):
        debug.append(lambda screen: pygame.draw.circle(screen, color.to_tuple(), position.to_tuple(), radius, width))


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


class Text:
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
        texts.append(self)

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


def init():
    pygame.init()


class Window:
    def __init__(self, width: int = 0, height: int = 0, title: str = "Game Window", icon: str = None,
                 flags: Union[list[int], int] = 0,
                 depth: int = 0, display: int = 0, vsync: bool = False):
        Input.update()
        self.running = True
        totalFlags = 0
        if type(flags) is not int:
            for flag in flags:
                totalFlags |= flag
        else:
            totalFlags = flags

        self.screen = pygame.display.set_mode((width, height), totalFlags, depth, display, 1 if vsync else 0)
        self.width, self.height = pygame.display.get_window_size()
        self.icon = icon
        self.title = title
        if icon is not None:
            self.set_icon(icon)
        self.set_title(title)

        self.bgColor = Colors.white
        Input.update()  # can't figure out why I need 2 Input.Update(). It just works like that

    def fill_bg(self, color):
        if self.running:
            self.screen.fill(color.to_tuple())

    def set_bg(self, color):
        self.bgColor = color

    def set_title(self, title):
        self.title = title
        pygame.display.set_caption(title)

    def set_icon(self, icon):
        self.icon = pygame.image.load(icon)
        pygame.display.set_icon(self.icon)

    def update(self):
        global debug
        if self.running:
            self.width, self.height = pygame.display.get_window_size()
            if Input.get_event(QUIT):
                self.quit()
                return

            self.fill_bg(self.bgColor)

            for txt in texts:
                txt.set_text(txt.text)
                size = pygame.transform.rotate(txt.renderText, txt.rectTransform.rotation).get_rect().size
                self.screen.blit(pygame.transform.rotate(txt.renderText, -txt.rectTransform.rotation),
                                 (int(txt.rectTransform.position.x) - int(size[0] / 2),
                                  int(txt.rectTransform.position.y) - int(size[1] / 2)))

            for obj in objects:
                size = pygame.transform.rotate(obj.Img, obj.transform.rotation).get_rect().size
                self.screen.blit(pygame.transform.rotate(obj.Img, -obj.transform.rotation),
                                 (int(obj.transform.position.x) - int(size[0] / 2),
                                  int(obj.transform.position.y) - int(size[1] / 2)))

            for game_object in game_objects:
                game_object.update(self.screen)

            for obj in lambdas:
                if hasattr(obj, "rigidbody"):
                    obj.rigidbody.update_action()

            for key in lambdas:
                lambdas[key](self.screen, key)

            for func in debug:
                func(self.screen)

            debug = []

            Input.update()
            pygame.display.flip()
            RealTime.wait_for_real_time(RealTime.delta_time)

    def quit(self):
        self.running = False
        pygame.quit()


# colors

keys = []
oldKeys = []
events = []


class Input:
    @staticmethod
    def get_key(key) -> bool:
        return keys[key]

    @staticmethod
    def get_key_down(key) -> bool:
        return (not oldKeys[key]) and keys[key]

    @staticmethod
    def get_key_up(key) -> bool:
        return oldKeys[key] and not keys[key]

    @staticmethod
    def get_event(event, attribute: str = "", value=None) -> bool:
        b = False
        for ev in events:
            if ev.type == event:
                if attribute == "":
                    b = True
                else:
                    if getattr(ev, attribute) == value:
                        b = True
        return b

    @staticmethod
    def get_event_property(event, prop: str):
        for ev in events:
            if ev.type == event:
                return getattr(ev, prop)
        raise Exception(f"Event '{event}' doesn't exist. Maybe doesn't happen every frame?")

    # Mouse
    @staticmethod
    def get_mouse_button_down(button) -> bool:
        return Input.get_event(MOUSEBUTTONDOWN, "button", button)

    @staticmethod
    def get_mouse_button_up(button) -> bool:
        return Input.get_event(MOUSEBUTTONUP, "button", button)

    @staticmethod
    def get_mouse_position() -> Vector2:
        pos = pygame.mouse.get_pos()
        return Vector2(pos[0], pos[1])

    @staticmethod
    def update():
        global keys, events, oldKeys
        oldKeys = keys
        keys = pygame.key.get_pressed()
        events = pygame.event.get()


quitting = False


class RealTime:
    t = time.monotonic()  # init time
    delta_time = 1 / 60

    @staticmethod
    def set_dt(dt):
        RealTime.delta_time = dt

    @staticmethod
    def wait_for_real_time(dt):
        RealTime.t = RealTime.t + dt
        wait = RealTime.t - time.monotonic()
        if wait > 0:
            time.sleep(wait)
