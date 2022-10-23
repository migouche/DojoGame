from dojogame.dojographics.gameobjects import GameObject, Polygon, Circle
from dojogame.dojomaths.vectors import Vector2


class Collision:
    def __init__(self, collide: bool, point: Vector2 = None, normal: Vector2 = None):
        self.collide = collide
        self.point = point
        self.normal = normal

    def __bool__(self):
        return self.collide


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
    def point_inside_polygon(point: Vector2, polygon: Polygon) -> bool:
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
    def find_arithmetic_mean(points: list) -> Vector2:
        x = y = 0

        for j in range(len(points)):
            x += points[j].x
            y += points[j].y
        return Vector2(x / len(points), y / len(points))

    @staticmethod
    def intersect_polygons(p1: Polygon, p2: Polygon) -> Collision:
        if not p1.get_collider().aabb.aabb_overlap(p2.get_collider().aabb):
            return Collision(False)

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
            normal = -normal
        return Collision(True, normal=normal)

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
    def gjk(p1: Polygon, p2: Polygon) -> Collision:
        if not p1.get_collider().aabb.aabb_overlap(p2.get_collider().aabb):
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
    def intersect_circles(c1: Circle, c2: Circle) -> Collision:
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
    def intersect_circle_polygon(circle: Circle, polygon: Polygon) -> Collision:
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

        closest_point = Collisions.find_closest_point_on_polygon(circle.transform.position, polygon)
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

        return Collision(True, circle.transform.position + normal * depth, normal)


class Collider:

    def __init__(self, object: GameObject):
        self.aabb = AABB(object)

    def collide_with(self, other) -> Collision:
        raise NotImplementedError

    @staticmethod
    def add_collider(go: GameObject):
        if isinstance(go, Polygon):
            go.collider = PolygonCollider(go)
        elif isinstance(go, Circle):
            go.collider = CircleCollider(go)
        else:
            raise TypeError("Wrong type of object given")


class PolygonCollider(Collider):
    def __init__(self, polygon: Polygon):
        super().__init__(polygon)
        self.polygon = polygon

    def collide_with(self, other: Collider) -> bool:
        if other is None:
            return False
        if isinstance(other, PolygonCollider):
            return bool(Collisions.intersect_polygons(self.polygon, other.polygon))
        else:
            raise NotImplementedError


class CircleCollider(Collider):
    def __init__(self, circle: Circle):
        super().__init__(circle)
        self.circle = circle

    def collide_with(self, other) -> Collision:
        if isinstance(other, CircleCollider):
            return Collisions.intersect_circles(self.circle, other.circle)
        else:
            return Collisions.intersect_circle_polygon(self.circle, other.polygon)
