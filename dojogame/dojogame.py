import math
import random
import time
from enum import Enum
from typing import Union

import pygame
from pygame.constants import *


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, v):
        return Vector2(self.x + v.x, self.y + v.y)

    def __sub__(self, v):
        return Vector2(self.x - v.x, self.y - v.y)

    def __mul__(self, f):
        return Vector2(self.x * f, self.y * f)

    def __truediv__(self, f):
        return Vector2(self.x / f, self.y / f)

    def __str__(self):
        return "Vector2:(" + str(self.x) + ", " + str(self.y) + ")"

    def __eq__(self, v):
        return self.x == v.x and self.y == v.y

    def to_tuple(self):
        return self.x, self.y

    @staticmethod
    def zero():
        return Vector2(0, 0)

    @staticmethod
    def dot(a, b):
        return a.x * b.x + a.y * b.y

    @staticmethod
    def cross(a, b):
        return a.x * b.y - b.x * a.y

    @staticmethod
    def scale(a, b):
        return Vector2(a.x * b.x, a.y * b.y)

    @staticmethod
    def angle_rad(a, b):
        return math.atan2(Vector2.cross(a, b), Vector2.dot(a, b))

    @staticmethod
    def angle_deg(a, b):
        return Vector2.angle_rad(a, b) * Mathf.Rad2Deg

    def to_vector2_int(self):
        return Vector2Int(int(self.x), int(self.y))

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    @staticmethod
    def distance(a, b):
        return (b - a).magnitude()

    def normalized(self):
        return self / self.magnitude()

    @staticmethod
    def from_angle_rad(angle):
        return Vector2(math.cos(angle), math.sin(angle))

    @staticmethod
    def from_angle_deg(angle):
        return Vector2.from_angle_rad(angle * Mathf.Deg2Rad)

    @staticmethod
    def random():
        return Vector2.rad_random(0, 6.28)

    @staticmethod
    def deg_random(a, b):
        return Vector2.rad_random(a * Mathf.Deg2Rad, b * Mathf.Deg2Rad)

    @staticmethod
    def rad_random(a, b):
        return Vector2.from_angle_rad(random.randint(int(a * 100), int(b * 100)) / 100).normalized()


class Vector2Int:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __add__(self, v):
        return Vector2Int(self.x + v.x, self.y + v.y)

    def __sub__(self, v):
        return Vector2Int(self.x - v.x, self.y - v.y)

    def __mul__(self, f):
        return Vector2Int(self.x * f, self.y * f)

    def __truediv__(self, f):
        return Vector2Int(self.x / f, self.y / f)

    def __str__(self):
        return "Vector2Int:(" + str(self.x) + ", " + str(self.y) + ")"

    def __eq__(self, v):
        return self.x == v.x and self.y == v.y

    @staticmethod
    def zero():
        return Vector2(0, 0)

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    @staticmethod
    def distance(a, b):
        return (b - a).magnitude()

    def normalized(self):
        return self / self.magnitude()


objects = []
texts = []
debug = []
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


class Raycast:
    @staticmethod
    def raycast(start: Vector2, _dir: Union[float, Vector2], length: float = None):
        pos = start
        step = 0
        while (length is None or Vector2.distance(pos, start) < length) and (  # checks for length and for inside screen
                0 < pos.x < pygame.display.get_window_size()[0] and
                0 < pos.y < pygame.display.get_window_size()[1]):
            pos = start + _dir * step

            for obj in lambdas:
                if hasattr(obj, 'collider') and obj.collider.hit_inside_collider(pos):
                    return obj.collider.hit_inside_collider(pos)
            step += 1
        return RaycastHit(False)


class RaycastHit:
    def __init__(self, collide: bool, point: Vector2 = None, normal: Vector2 = None, dist: float = None, collider=None):
        self.collide = collide
        self.point = point
        self.normal = normal
        self.distance = dist
        self.collider = collider

    def __bool__(self):
        return self.collide


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

        posRel = position if space == Space.Self else \
            position - self.object.transform.position if space == Space.World else None

        if posRel is None:
            raise TypeError("Wrong Space given")

        if mode == ForceMode.Force:  # dv = F * dt / m
            self.totalAction += Action(f := force * RealTime.deltaTime / self.mass, Vector2.cross(posRel, f))
        elif mode == ForceMode.Acceleration:  # dv = F * dt
            self.totalAction += Action(f := force * RealTime.deltaTime, Vector2.cross(posRel, f))
        elif mode == ForceMode.Impulse:  # dv = F / m
            self.totalAction += Action(f := force / self.mass, Vector2.cross(posRel, f))
        elif mode == ForceMode.VelocityChange:  # dv = F
            self.totalAction += Action(f := force, Vector2.cross(posRel, f))
        else:
            raise TypeError("Wrong ForceMode given")

    def add_force(self, force: Vector2, mode: ForceMode = ForceMode.Force):
        self.add_force_at_position(force, self.object.transform.position, mode)

    def update_action(self):
        self.velocity += self.totalAction.dSpeed
        self.angularVelocity += self.totalAction.dAngle

        self.object.transform.position += self.velocity * RealTime.deltaTime
        self.object.transform.rotation += self.angularVelocity * RealTime.deltaTime

        self.totalAction = Action()


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


class Collision:
    def __init__(self, collide: bool, point: Vector2 = None, normal: Vector2 = None):
        self.collide = collide
        self.point = point
        self.normal = normal

    def __bool__(self):
        return self.collide


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


class Circle(BaseObject):
    def __init__(self, radius: int, mass: float = 1, outline: int = 0, color: Color = Colors.black,
                 position: Vector2 = Vector2.zero(), rotation: float = 0):
        super().__init__(lambda screen, obj: pygame.draw.circle(screen,
                                                                obj.color.to_tuple(),
                                                                obj.transform.position.to_tuple(),
                                                                obj.radius, obj.outline),
                         mass, position, rotation, CircleCollider, color, self, radius=radius,
                         outline=outline)


class CircleCollider(BaseCollider):
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
            vertices = self.object.getVertices()
            for v in vertices:
                if hit := other.collider.hitInsideCollider(v):
                    return Collision(True, v, hit.normal)
            try:
                return other.collider.tryReverseCollision(self.object)
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


class Transform:
    def __init__(self, pos: Vector2 = Vector2.zero(), angle: float = 0, scale: Vector2 = Vector2.zero()):
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
            RealTime.wait_for_real_time(RealTime.deltaTime)

    def quit(self):
        self.running = False
        pygame.quit()


# colors

keys = []
oldKeys = []
events = []


class Input:
    @staticmethod
    def get_key(key):
        return keys[key]

    @staticmethod
    def get_key_down(key):
        return (not oldKeys[key]) and keys[key]

    @staticmethod
    def get_key_up(key):
        return oldKeys[key] and not keys[key]

    @staticmethod
    def get_event(event, attribute: str = "", value=None):
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
    def get_mouse_button_down(button):
        return Input.get_event(MOUSEBUTTONDOWN, "button", button)

    @staticmethod
    def get_mouse_button_up(button):
        return Input.get_event(MOUSEBUTTONUP, "button", button)

    @staticmethod
    def get_mouse_position():
        pos = pygame.mouse.get_pos()
        return Vector2(pos[0], pos[1])

    @staticmethod
    def update():
        global keys, events, oldKeys
        oldKeys = keys
        keys = pygame.key.get_pressed()
        events = pygame.event.get()


class Mathf:
    @staticmethod
    def clamp(value, Min, Max):
        if value <= Min:
            return Min
        elif value >= Max:
            return Max
        else:
            return value

    Deg2Rad = math.pi / 180
    Rad2Deg = 1 / Deg2Rad


quitting = False


class RealTime:
    t = time.monotonic()  # init time
    deltaTime = 1 / 60

    @staticmethod
    def set_dt(dt):
        RealTime.deltaTime = dt

    @staticmethod
    def wait_for_real_time(dt):
        RealTime.t = RealTime.t + dt
        wait = RealTime.t - time.monotonic()
        if wait > 0:
            time.sleep(wait)
