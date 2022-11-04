import math

from dojogame.maths.vectors import Vector2
from dojogame.data.enums import Space, ForceMode
from dojogame.maths.realtime import RealTime
from dojogame.graphics.gameobjects import GameObject


#  requires A LOT of rework

class Action:
    def __init__(self, dSpeed: Vector2 = Vector2.zero(), dAngle: float = 0):
        self.dSpeed = dSpeed
        self.dAngle = dAngle

    def __add__(self, other) -> 'Action':
        return Action(self.dSpeed + other.dSpeed, self.dAngle + other.dAngle)


class Rigidbody:
    def __init__(self, game_object: GameObject, mass: float = 1):
        self.game_object = game_object
        self.totalAction = Action()
        self.velocity = Vector2.zero()
        self.angularVelocity = 0
        self.mass = mass
        self.kinematic = False
        self.useGravity = False  # May use it later, may not

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
        self.add_force_at_position(force, self.game_object.transform.position, mode)

    def update_action(self):
        self.velocity += self.totalAction.dSpeed
        self.angularVelocity += self.totalAction.dAngle

        self.game_object.transform.position += self.velocity * RealTime.delta_time
        self.game_object.transform.rotation += self.angularVelocity * RealTime.delta_time

        self.totalAction = Action()

    @staticmethod
    def add_rigidbody(game_object, mass: float = 1) -> GameObject:
        game_object._rigidbody = Rigidbody(game_object, mass)
        return game_object


class AngularInertia:
    @staticmethod
    def calculate_moment_of_inertia(points: list[Vector2], density: float) -> float:
        if len(points) < 3:
            raise TypeError("Must have at least 3 points")
        moment_of_inertia = 0
        for i in range(1, len(points) - 1):
            p1 = points[0]
            p2 = points[i]
            p3 = points[i + 1]

            w = Vector2.distance(p1, p2)
            w1 = abs(Vector2.dot(p1 - p2, p3 - p2) / w)
            w2 = abs(w - w1)

            signed_tri_area = Vector2.cross(p3 - p1, p2 - p1) / 2
            h = 2 * abs(signed_tri_area) / w

            p4 = p2 + (p1 - p2) * w1 / w

            cm1 = (p2 + p3 + p4) / 3
            cm2 = (p1 + p3 + p4) / 3

            i1 = density * w1 * h * ((h * h / 4) + (w1 * w1 / 12))
            i2 = density * w2 * h * ((h * h / 4) + (w2 * w2 / 12))
            m1 = w1 * h * density / 2
            m2 = w2 * h * density / 2

            i1cm = i1 + m1 * Vector2.distance(cm1, p3) ** 2  # TODO: remove square of root
            i2cm = i2 + m2 * Vector2.distance(cm2, p3) ** 2  # TODO: remove square of root

            moment_of_inertia1 = i1cm + m1 * Vector2.distance(cm1, p4) ** 2
            moment_of_inertia2 = i2cm + m2 * Vector2.distance(cm2, p4) ** 2

            if Vector2.cross(p1 - p3, p4 - p3) > 0:
                moment_of_inertia += moment_of_inertia1
            else:
                moment_of_inertia -= moment_of_inertia1
            if Vector2.cross(p4 - p3, p2 - p3) > 0:
                moment_of_inertia += moment_of_inertia2
            else:
                moment_of_inertia -= moment_of_inertia2
        return abs(moment_of_inertia)

    @staticmethod
    def calculate_moment_of_inertia2(_points: list[Vector2], mass: float) -> float:
        if len(_points) < 3:
            raise TypeError("Must have at least 3 points")
        points = _points.copy()


        area = 0
        center = Vector2.zero()
        mmoi = 0

        prev = -1
        for i in range(len(points)):
            print(f"prev: {prev}, i: {i}")
            a = points[prev]
            b = points[i]

            area_step = Vector2.cross(a, b) / 2
            center_step = (a + b) / 3
            mmoi_step = area_step * (Vector2.dot(a, a) + Vector2.dot(b, b) + Vector2.dot(a, b)) / 6
            try:
                center = (center * area + center_step * area_step) / (area + area_step)
            except ZeroDivisionError:
                center = center_step
            area += area_step
            mmoi += mmoi_step

            prev = i
        density = mass / area
        mmoi *= density
        mmoi -= mass * Vector2.dot(center, center)
        return abs(mmoi)

    class Inertia:
        def __init__(self, mass: float):
            self.mass = mass
            self.density = self.calculate_density()

        def calculate_density(self):
            raise NotImplementedError

    class RecTriangle(Inertia):
        def __init__(self, base: float, height: float, mass: float):
            self.base = base
            self.height = height
            super().__init__(mass)

        def calculate_density(self):
            return 2 * self.mass / (self.base * self.height)

        @property
        def inertia(self) -> float:
            return self.density * (self.height * self.base ** 3 / 4 + self.base * self.height ** 3 / 12)

    class Triangle(Inertia):
        def __init__(self, vertices: list[Vector2], mass: float):
            if len(vertices) != 3:
                raise TypeError("Triangle must have 3 vertices")
            self.vertices = vertices
            super().__init__(mass)

        def calculate_density(self):
            return 2 * self.mass / Vector2.cross(self.vertices[1] - self.vertices[0],
                                                 self.vertices[2] - self.vertices[0])

        def triangles(self) -> tuple:
            p1, p2, p3 = self.vertices
            v1 = p2 - p1
            v2 = p3 - p1
            p4 = p1 + Vector2.cross(v2, v1) / v1.magnitude() ** 2 * v1
            return AngularInertia.RecTriangle(
                (p4 - p1).magnitude(),
                (p4 - p3).magnitude(),
                self.density), AngularInertia.RecTriangle(
                (p2 - p1).magnitude(),
                (p4 - p3).magnitude(),
                self.density)

        @property
        def inertia(self) -> float:
            p1, p2, p3 = self.vertices
            v1 = p2 - p1
            v2 = p3 - p1
            p4 = p1 + v1 * Vector2.cross(v2, v1) / v1.magnitude() ** 2
            i = 1
            i = math.copysign(i, Vector2.cross(p4 - p1, p3 - p1))
            return abs((tri := self.triangles())[0].inertia + i * tri[1].inertia)

    class Polygon(Inertia):
        def __init__(self, vertices: list[Vector2], mass: float):
            if len(vertices) < 4:
                raise TypeError("Polygon must have at least 4 vertices")
            self.vertices = vertices
            super().__init__(mass)

        def calculate_density(self):
            return 2 * self.mass / sum(Vector2.cross(self.vertices[i] - self.vertices[0],
                                                     self.vertices[i + 1] - self.vertices[0])
                                       for i in range(len(self.vertices) - 1))

        @property
        def inertia(self) -> float:
            # return sum([AngularInertia.Triangle([self.vertices[0], self.vertices[i], self.vertices[i + 1]],
            #                                    self.density).inertia for i in range(1, len(self.vertices) - 1)])
            inertia = 0
            for i in range(1, len(self.vertices) - 1):
                inertia += AngularInertia.Triangle([self.vertices[0], self.vertices[i], self.vertices[i + 1]],
                                                   self.density).inertia
            return inertia
