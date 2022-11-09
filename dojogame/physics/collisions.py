import array

from dojogame.graphics.gameobjects import GameObject, Polygon, Circle
from dojogame.maths.vectors import Vector2


class AxisAlignedBoundingBox:
    def __init__(self, obj: GameObject):
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
            self.min_v = self.obj.transform.position - \
                         Vector2(self.obj.radius, self.obj.radius)

            self.max_v = self.obj.transform.position + \
                         Vector2(self.obj.radius, self.obj.radius)
        else:
            raise TypeError("Wrong type of object given")

    def aabb_overlap(self, other: 'AxisAlignedBoundingBox') -> bool:
        return self.min_v.x < other.max_v.x and self.max_v.x > other.min_v.x and \
               self.min_v.y < other.max_v.y and self.max_v.y > other.min_v.y


AABB = AxisAlignedBoundingBox


class Collisions:
    @staticmethod
    def point_inside_polygon(point: Vector2, polygon: 'PolygonCollider') -> bool:
        if polygon is None:
            raise TypeError("Polygon has no collider")
        polygon = polygon.game_object

        if not isinstance(polygon, Polygon):
            raise TypeError("Collider must be attached to a Polygon")

        c = False
        vertices = polygon.get_absolute_vertices_positions()

        for i in range(len(vertices)):
            j = (i + 1) % len(vertices)
            if ((vertices[i].y > point.y) != (vertices[j].y > point.y)) and \
                    (point.x < (vertices[j].x - vertices[i].x) * (point.y - vertices[i].y) /
                     (vertices[j].y - vertices[i].y) + vertices[i].x):
                c = not c
        return c

    @staticmethod
    def point_inside_circle(point: Vector2, circle: 'CircleCollider') -> bool:
        if circle is None:
            raise TypeError("Circle has no collider")

        circle = circle.game_object

        if not isinstance(circle, Circle):
            raise TypeError("Collider must be attached to a circle")

        return (point - circle.transform.position).magnitude <= circle.radius

    @staticmethod
    def find_arithmetic_mean(points: list) -> Vector2:
        x = y = 0

        for j in range(len(points)):
            x += points[j].x
            y += points[j].y
        return Vector2(x / len(points), y / len(points))

    @staticmethod
    def intersect_polygons(c1: 'PolygonCollider', c2: 'PolygonCollider') -> 'Collision':
        if not c1.aabb.aabb_overlap(c2.aabb):
            return Collision(False)

        p1 = c1.game_object
        p2 = c2.game_object

        if not isinstance(p1, Polygon) or not isinstance(p2, Polygon):
            raise TypeError("Colliders must be attached to polygons")

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

        center_a = Collisions.find_arithmetic_mean(vertices_a)
        center_b = Collisions.find_arithmetic_mean(vertices_b)

        direction = center_b - center_a

        if Vector2.dot(direction, normal) < 0:
            normal = -normal  # normal will be used for continuous collision detection,
            # doesn't make sense to use it with static collision detection

        points = []
        for i in range(len(vertices_a)):
            for j in range(len(vertices_b)):
                if col := Collisions.segment_intersect_segment(vertices_a[i], vertices_a[(i + 1) % len(vertices_a)],
                                                               vertices_b[j], vertices_b[(j + 1) % len(vertices_b)]):
                    points.append(col.get_contact(0))
        return Collision(True, points, collider=c2)

    @staticmethod
    def contains_origin(vertices: list) -> bool:
        """
        Checks if a polygon contains the origin
        :param vertices: list of vertices
        :return: bool
        """
        intersections = 0
        for i in range(len(vertices)):
            va = vertices[i]
            vb = vertices[(i + 1) % len(vertices)]
            if va.y > 0 != vb.y > 0:
                if va.x < 0 or vb.x < 0:
                    if va.x + (0 - va.y) / (vb.y - va.y) * (vb.x - va.x) < 0:
                        intersections += 1
        return intersections % 2 == 1

    @staticmethod
    def simplex(vertices: list, axis: Vector2) -> tuple:
        min_v = max_v = Vector2.dot(vertices[0], axis)
        for vertex in vertices:
            projection = Vector2.dot(vertex, axis)
            if projection < min_v:
                min_v = projection
            if projection > max_v:
                max_v = projection
        return min_v, max_v

    @staticmethod
    def support(vertices_a: list, vertices_b: list, axis: Vector2) -> Vector2:
        max_a = max_b = Vector2.dot(vertices_a[0], axis)
        max_vertex_a = vertices_a[0]
        max_vertex_b = vertices_b[0]
        for vertex in vertices_a:
            projection = Vector2.dot(vertex, axis)
            if projection > max_a:
                max_a = projection
                max_vertex_a = vertex
        for vertex in vertices_b:
            projection = Vector2.dot(vertex, axis)
            if projection > max_b:
                max_b = projection
                max_vertex_b = vertex
        return max_vertex_a - max_vertex_b

    @staticmethod
    def gjk(p1: Polygon, p2: Polygon) -> 'Collision':
        if not p1.collider.aabb.aabb_overlap(p2.collider.aabb):
            return Collision(False)

        vertices_a = p1.get_absolute_vertices_positions()
        vertices_b = p2.get_absolute_vertices_positions()

        center_a = Collisions.find_arithmetic_mean(vertices_a)
        center_b = Collisions.find_arithmetic_mean(vertices_b)

        direction = center_b - center_a

        simplex = [Collisions.support(vertices_a, vertices_b, direction)]

        direction = -simplex[0]

        while True:
            simplex.append(Collisions.support(vertices_a, vertices_b, direction))

            if Vector2.dot(simplex[-1], direction) < 0:
                return Collision(False)

            if Collisions.contains_origin(simplex):
                return Collision(True)

    @staticmethod
    def intersect_circles(c1: 'CircleCollider', c2: 'CircleCollider') -> 'Collision':
        c1 = c1.game_object
        c2 = c2.game_object
        if not isinstance(c1, Circle) or not isinstance(c2, Circle):
            raise TypeError("Colliders must be attached to circles")

        distance = Vector2.distance(c1.transform.position, c2.transform.position)
        if distance > c1.radius + c2.radius:
            return Collision(False)
        normal = (c1.transform.position - c2.transform.position).normalized()
        point = ((c1.transform.position - normal * c1.radius) -
                 (c2.transform.position + normal * c2.radius)) / 2
        return Collision(True, point, normal)

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

    @staticmethod
    def find_closest_point_on_polygon(point: Vector2, polygon: Polygon) -> Vector2:
        vertices = polygon.get_absolute_vertices_positions()
        result = Vector2(None, None)
        min_distance = float('inf')

        for v in vertices:
            if dist := Vector2.distance(point, v) < min_distance:
                min_distance = dist
                result = v

        return result

    @staticmethod
    def project_circle(circle: Circle, axis: Vector2) -> tuple:
        dir_radius = axis.normalized() * circle.radius

        p1 = circle.transform.position + dir_radius
        p2 = circle.transform.position - dir_radius

        min_ = Vector2.dot(p1, axis)
        max_ = Vector2.dot(p2, axis)

        if min_ > max_:
            min_, max_ = max_, min_

        return min_, max_

    @staticmethod
    def intersect_circle_polygon(circle: 'CircleCollider', polygon: 'PolygonCollider') -> 'Collision':

        circle = circle.game_object
        polygon = polygon.game_object

        if not isinstance(circle, Circle) or not isinstance(polygon, Polygon):
            raise TypeError('Circle and Polygon must be instances of Circle and Polygon')

        if not circle.collider.aabb.aabb_overlap(polygon.collider.aabb):
            return Collision(False)

        vertices = polygon.get_absolute_vertices_positions()
        normal = Vector2.zero()
        depth = float('inf')

        for i in range(len(vertices)):
            va = vertices[i]
            vb = vertices[(i + 1) % len(vertices)]

            edge = vb - va
            axis = Vector2(-edge.y, edge.x)

            (min_a, max_a) = Collisions.project_vertices(vertices, axis)
            (min_b, max_b) = Collisions.project_circle(circle, axis)

            if min_a >= max_b or min_b >= max_a:
                return Collision(False)

            axis_depth = min(max_a - min_b, max_b - min_a)

            if axis_depth < depth:
                depth = axis_depth
                normal = axis

        closest_point = Collisions. \
            find_closest_point_on_polygon(circle.transform.position, polygon)
        axis = closest_point - circle.transform.position

        (min_a, max_a) = Collisions.project_vertices(vertices, axis)
        (min_b, max_b) = Collisions.project_circle(circle, axis)

        if min_a >= max_b or min_b >= max_a:
            return Collision(False)

        axis_depth = min(max_a - min_b, max_b - min_a)

        if axis_depth < depth:
            depth = axis_depth
            normal = axis

        depth /= normal.magnitude()
        normal = normal.normalized()

        polygon_center = Collisions.find_arithmetic_mean(vertices)
        direction = polygon_center - circle.transform.position

        if Vector2.dot(direction, normal) < 0:
            normal = -normal

        return Collision(True, circle.transform.position + normal * depth, normal)  # TODO: this will give error

    @staticmethod
    def segment_intersect_segment(a1: Vector2, a2: Vector2, b1: Vector2, b2: Vector2) -> 'Collision':
        s1 = a2 - a1
        s2 = b2 - b1

        d = -s2.x * s1.y + s1.x * s2.y
        if d == 0:
            return Collision(False)

        s = (-s1.y * (a1.x - b1.x) + s1.x * (a1.y - b1.y)) / d
        t = (s2.x * (a1.y - b1.y) - s2.y * (a1.x - b1.x)) / d

        if 0 <= s <= 1 and 0 <= t <= 1:
            p = ContactPoint(a1 + (t * s1), (b2 - b1).
                             left_perpendicular().normalized())  # TODO: you're better than this
            return Collision(True, [p])
        return Collision(False)


class Collider:

    def __init__(self, game_object: GameObject):
        self.game_object = game_object
        self.aabb = AABB(game_object)

    def collide_with(self, other) -> 'Collision':
        raise NotImplementedError

    def point_inside_collider(self, point: Vector2) -> bool:
        raise NotImplementedError

    @staticmethod
    def add_collider(go: GameObject) -> GameObject:
        if isinstance(go, Polygon):
            go._collider = PolygonCollider(go)
        elif isinstance(go, Circle):
            go._collider = CircleCollider(go)
        else:
            raise TypeError("Wrong type of object given")
        return go


class PolygonCollider(Collider):
    def __init__(self, polygon: Polygon):
        super().__init__(polygon)

    def point_inside_collider(self, point: Vector2) -> bool:
        return Collisions.point_inside_polygon(point, self)

    def collide_with(self, other: Collider) -> 'Collision':
        if other is None:
            return Collision(False)
        if isinstance(other, PolygonCollider):
            return Collisions.intersect_polygons(self, other)
        else:
            raise NotImplementedError


class CircleCollider(Collider):
    def __init__(self, circle: Circle):
        super().__init__(circle)

    def point_inside_collider(self, point: Vector2) -> bool:
        return Collisions.point_inside_circle(point, self)

    def collide_with(self, other) -> 'Collision':
        if isinstance(other, CircleCollider):
            return Collisions.intersect_circles(self.game_object.collider, other.game_object.collider)
        else:
            return Collisions.intersect_circle_polygon(self.game_object.collider, other.polygon.collider)


class ContactPoint:
    def __init__(self, point: Vector2, normal: Vector2, other_collider: Collider = None):
        self.point = point
        self.normal = normal
        self.other_collider = other_collider


class Collision:
    def __init__(self, collide: bool, contacts: ['ContactPoint'] = None, collider: Collider = None):
        self.collide = collide
        self.contacts = [] if contacts is None else contacts
        self.contact_count = len(contacts) if contacts is not None else 0
        self.collider = collider

        self.game_object = self.rigidbody = self.transform = None

        if isinstance(collider, PolygonCollider):
            self.game_object = collider.game_object
        elif isinstance(collider, CircleCollider):
            self.game_object = collider.game_object

        if self.game_object is not None:
            try:
                self.rigidbody = self.game_object.rigidbody
            except AttributeError:
                self.rigidbody = None
            self.transform = self.game_object.transform

        self.impulse = Vector2.zero()
        self.relative_velocity = Vector2.zero()

    def get_contacts(self) -> [ContactPoint]:
        return self.contacts

    def get_contact(self, index: int) -> ContactPoint:
        return self.contacts[index]

    def __bool__(self):
        return self.collide
