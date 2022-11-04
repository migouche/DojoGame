import math

from dojogame.maths.vectors import Vector2
from dojogame.data.enums import Space, ForceMode
from dojogame.maths.realtime import RealTime
from dojogame.graphics.gameobjects import GameObject, Polygon


#  requires A LOT of rework

class Action:
    def __init__(self, dSpeed: Vector2 = Vector2.zero(), dAngle: float = 0):
        self.d_speed = dSpeed
        self.d_angle = dAngle

    def __add__(self, other: 'Action') -> 'Action':
        return Action(self.d_speed + other.d_speed, self.d_angle + other.d_angle)


class Rigidbody:
    def __init__(self, game_object: GameObject, mass: float = 1):
        self.game_object = game_object
        self.total_action = Action()
        self.velocity = Vector2.zero()
        self.angular_velocity = 0
        self.mass = mass
        self.kinematic = False
        self.use_gravity = False  # May use it later, may not
        self.local_center_of_mass = Vector2.zero()
        self.relocate_vertices()
        self.moment_of_inertia = AngularInertia.calculate_moment_of_inertia(
            self.game_object.local_vertices_positions, self.mass) \
            if isinstance(self.game_object, Polygon) else 1

    def relocate_vertices(self):
        if not isinstance(self.game_object, Polygon):
            raise TypeError("Rigidbody must be attached to a Polygon")
        self.local_center_of_mass = AngularInertia.calculate_centroid(self.game_object.local_vertices_positions)
        self.game_object.local_vertices_positions = [v - self.local_center_of_mass for v in
                                                     self.game_object.local_vertices_positions]

    def add_force_at_position(self, force: Vector2, position: Vector2,
                              mode: ForceMode = ForceMode.Force,
                              space: Space = Space.World):

        if space == Space.Self:
            absolute_pos = self.game_object.transform.relative_pos_to_absolute(position)
            absolute_force = Vector2.rotate_by_degs(force, self.game_object.transform.rotation)

            self.add_force_at_position(absolute_force, absolute_pos, mode, Space.World)
            return
        pos_rel = position - self.game_object.transform.position if space == Space.World else None
        if pos_rel is None:
            raise TypeError("Wrong Space given")

        if mode == ForceMode.Force:  # dv = F * dt / m
            self.total_action += Action(f := force * RealTime.delta_time / self.mass, Vector2.cross(pos_rel, f))
        elif mode == ForceMode.Acceleration:  # dv = F * dt
            self.total_action += Action(f := force * RealTime.delta_time, Vector2.cross(pos_rel, f))
        elif mode == ForceMode.Impulse:  # dv = F / m
            self.total_action += Action(f := force / self.mass, Vector2.cross(pos_rel, f))
        elif mode == ForceMode.VelocityChange:  # dv = F
            self.total_action += Action(f := force, Vector2.cross(pos_rel, f))
        else:
            raise TypeError("Wrong ForceMode given")

    def add_force(self, force: Vector2, mode: ForceMode = ForceMode.Force):
        self.add_force_at_position(force, self.game_object.transform.position, mode)

    def update_action(self):
        self.velocity += self.total_action.d_speed
        self.angular_velocity += self.total_action.d_angle

        self.game_object.transform.position += self.velocity * RealTime.delta_time
        self.game_object.transform.rotation += self.angular_velocity * RealTime.delta_time

        self.total_action = Action()

    @staticmethod
    def add_rigidbody(game_object, mass: float = 1) -> GameObject:
        game_object._rigidbody = Rigidbody(game_object, mass)
        return game_object


class AngularInertia:
    @staticmethod
    def calculate_centroid(vertices: list[Vector2]) -> Vector2:
        centroid = Vector2.zero()
        for vertex in vertices:
            centroid += vertex
        return centroid / len(vertices)

    @staticmethod
    def calculate_moment_of_inertia(_points: list[Vector2], mass: float) -> float:
        if len(_points) < 3:
            raise TypeError("Must have at least 3 points")
        centroid = AngularInertia.calculate_centroid(_points)
        points = []
        for point in _points:
            points.append(point - centroid)

        area = 0
        center = Vector2.zero()
        mmoi = 0

        prev = -1
        for i in range(len(points)):
            a = points[prev]
            b = points[i]

            area_step = Vector2.cross(a, b) / 2
            center_step = (a + b) / 3
            mmoi_step = area_step * (Vector2.dot(a, a) + Vector2.dot(b, b) + Vector2.dot(a, b)) / 6
            center = (center * area + center_step * area_step) / (area + area_step)

            area += area_step
            mmoi += mmoi_step

            prev = i
        density = mass / area
        mmoi *= density
        mmoi -= mass * Vector2.dot(center, center)
        return abs(mmoi)
