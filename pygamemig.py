import pygame
from pygame.constants import *
import math
import random
import time
from enum import Enum
from typing import Union


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

    def toTuple(self):
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
    def angleRad(a, b):
        return math.atan2(Vector2.cross(a, b), Vector2.dot(a, b))

    @staticmethod
    def angleDeg(a, b):
        return Vector2.angleRad(a, b) * Mathf.Rad2Deg

    def toVector2Int(self):
        return Vector2Int(int(self.x), int(self.y))

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def unit(self):
        return self / self.magnitude()

    @staticmethod
    def distance(a, b):
        return (b - a).magnitude()

    def normalized(self):
        return self / self.magnitude()

    @staticmethod
    def fromAngleRad(angle):
        return Vector2(math.cos(angle), math.sin(angle))

    @staticmethod
    def fromAngleDeg(angle):
        return Vector2.fromAngleRad(angle * Mathf.Deg2Rad)

    @staticmethod
    def random():
        return Vector2.radRandom(0, 6.28)

    @staticmethod
    def degRandom(a, b):
        return Vector2.radRandom(a * Mathf.Deg2Rad, b * Mathf.Deg2Rad)

    @staticmethod
    def radRandom(a, b):
        return Vector2.fromAngleRad(random.randint(int(a * 100), int(b * 100)) / 100).normalized()


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


class Color:
    def __init__(self, r: int, g: int, b: int, a:int = 255):
        self.red = r
        self.green = g
        self.blue = b
        self.alpha = a

    def __eq__(self, c):
        return self.red == c.red and self.green == c.green and self.blue == c.blue and self.alpha == c.alpha

    @staticmethod
    def fromHex(h):
        c = tuple(int(h.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
        return Color(c[0], c[1], c[2])

    def toTuple(self):
        return self.red, self.green, self.blue, self.alpha


class Colors:
    white = Color(255, 255, 255)
    black = Color(0, 0, 0)
    red = Color(255, 0, 0)
    green = Color(0, 255, 0)
    blue = Color(0, 0, 255)
    purple = Color(100, 0, 255)


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
    def regularPolygon(cls, scale):  # have to add sides parameter
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


class Rigidbody:
    def __init__(self, pos: Vector2 = Vector2.zero(), angle: float = 0):
        self.position = pos
        self.angle = angle
        self.velocity = Vector2.zero()
        self.kinematic = False

    def translate(self, pos: Vector2):
        self.position += pos

    def rotate(self, angle: float):
        self.angle += angle

    def rotateAroundOrigin(self, angle: float, origin: Vector2):
        s = math.sin(angle * Mathf.Deg2Rad)
        c = math.cos(angle * Mathf.Deg2Rad)

        point = self.position - origin

        self.position = Vector2(point.x * c - point.y * s + origin.x, point.x * s + point.y * c + origin.y)


class Circle:
    def __init__(self, radius: int, outline: int = 0, color: Color = Colors.black):
        self.rigidbody = Rigidbody()
        self.rigidbody.object = self
        self.radius = radius
        self.outline = outline
        self.color = color
        self.collider = CircleCollider(self)
        lambdas.update(
            {self.rigidbody: lambda screen, rb: pygame.draw.circle(screen,
                                                                   rb.object.color.toTuple(),
                                                                   (rb.position.x, rb.position.y),
                                                                   rb.object.radius, rb.object.outline)})


class Raycast:
    @staticmethod
    def raycast(start: Vector2, _dir: Union[float, Vector2], length: float = None):
        pos = start
        step = 0
        while (length is None or Vector2.distance(pos, start) < length) and (  # checks for length and for inside screen
                0 < pos.x < pygame.display.get_window_size()[0] and
                0 < pos.y < pygame.display.get_window_size()[1]):
            pos = start + _dir * step

            for rb in lambdas:
                if hasattr(rb.object, 'collider') and rb.object.collider.hitInsideCollider(pos):
                    return rb.object.collider.hitInsideCollider(pos)
            step += 1
        return RaycastHit(False)


class RaycastHit:
    def __init__(self, collide: bool, point: Vector2 = None, normal: Vector2 = None, dist: float = None):
        self.collide = collide
        self.point = point
        self.normal = normal
        self.distance = dist

    def __bool__(self):
        return self.collide


class CircleCollider:
    def __init__(self, circle: Circle):
        self.circle = circle

    def hitInsideCollider(self, point: Vector2):
        if Vector2.distance(self.circle.rigidbody.position, point) <= self.circle.radius:
            n = (point - self.circle.rigidbody.position).unit()
            return RaycastHit(True, self.circle.rigidbody.position + n * self.circle.radius, n,
                              Vector2.distance(self.circle.rigidbody.position, point))
        else:
            return RaycastHit(False)


class Rectangle:
    def __init__(self, w: int, h: int, color: Color = Colors.black):
        self.rigidbody = Rigidbody()
        self.width = w
        self.height = h
        self.color = color
        self.rigidbody.object = self
        self.collider = RectangleCollider(self)
        lambdas.update({self.rigidbody: lambda screen, rb: rb.object.draw(screen)})

    def draw(self, screen):  # doing this cause of not multi-line lambdas :v
        colorkey = Colors.white if self.color == Colors.black else Colors.black

        #  Message for future me: I went utra-instinct doing this, I don't remember what any of this means
        initSquare = pygame.Surface((self.width, self.height))
        initSquare.set_colorkey(colorkey.toTuple())
        initSquare.fill(self.color.toTuple())

        imgcopy = initSquare.copy()
        imgcopy.set_colorkey(colorkey.toTuple())
        rect = imgcopy.get_rect()
        rect.center = (self.rigidbody.position.x, self.rigidbody.position.y)
        old_center = rect.center
        rotSquare = pygame.transform.rotate(initSquare, -self.rigidbody.angle)
        rect = rotSquare.get_rect()
        rect.center = old_center
        screen.blit(rotSquare, rect)


class RectangleCollider:
    def __init__(self, rectangle: Rectangle):
        self.rectangle = rectangle

    def hitInsideCollider(self, point: Vector2):  # approximation with starting circle

        diagonal = math.sqrt(((self.rectangle.width / 2) ** 2) + ((self.rectangle.height / 2) ** 2))
        if Vector2.distance(self.rectangle.rigidbody.position, point) < diagonal:
            rb = Rigidbody(point)

            rb.rotateAroundOrigin(-self.rectangle.rigidbody.angle, self.rectangle.rigidbody.position)

            p = rb.position
            pos = self.rectangle.rigidbody.position

            # rectangle is horizontal: check for sides:

            w = self.rectangle.width
            h = self.rectangle.height

            if (pos.x - w / 2 < p.x < pos.x + w / 2 and
                    pos.y - h / 2 < p.y < pos.y + h / 2):  # we suppose we are in surface now
                offset = 1  # in pixels. Better if int
                normal = None
                if pos.y - (h/2 - offset) > p.y:
                    normal = Vector2(0, -1)
                elif pos.y + (h/2 - offset) < p.y:
                    normal = Vector2(0, 1)
                elif pos.x - (2/2 - offset) > p.x:
                    normal = Vector2(-1, 0)
                elif pos.x + (w/2 - offset) < p.x:
                    normal = Vector2(1, 0)
                else:
                    return RaycastHit(False)
                vec = Vector2.fromAngleDeg(Vector2.angleDeg(Vector2(1, 0), normal) + self.rectangle.rigidbody.angle)
                vecf = Vector2(vec.x, -vec.y)
                return RaycastHit(True, point, vec.unit())
            return RaycastHit(False)


class Square(Rectangle):
    def __init__(self, side: int, color: Color = Colors.black):
        super().__init__(side, side, color)


class Lines:
    @staticmethod
    def drawLine(_from: Vector2, _to: Vector2, width: int = 1, color: Color = Colors.black):
        debug.append(lambda screen: pygame.draw.line(screen, color.toTuple(), _from.toTuple(), _to.toTuple(), width))

    @staticmethod
    def drawRay(start: Vector2, _dir: Union[float, Vector2], length: int, width: int = 1, color: Color = Colors.black):
        vec = _dir.unit() * length if type(_dir) is Vector2 else Vector2.fromAngleDeg(_dir).unit() * length
        Lines.drawLine(start, start + vec, width, color)


class Transform:
    def __init__(self, pos, angle, scale):
        self.position = pos
        self.angle = angle
        self.scale = scale
        self.object = None

    def setPos(self, pos):
        self.position = pos

    def translate(self, translation):
        self.position += translation

    def setScale(self, scale):
        self.scale = scale
        self.Update()

    def setRot(self, angle):
        self.angle = angle % 360

    def rotate(self, angle):
        self.angle = (self.angle + angle) % 360

    def Update(self):
        self.object.offset = self.scale / 2
        self.object.Img = pygame.transform.scale(self.object.Img,
                                                 (self.scale.x,
                                                  self.scale.y))
        self.object.Img.get_rect()


class Text:
    def __init__(self, font, size, txtColor, bgColor):
        self.rectTransform = RectTransform(Vector2.zero(), 0)
        self.rectTransform.text = self
        self.text = ""
        self.size = size
        self.font = font
        self.textColor = txtColor
        self.BGColor = bgColor
        self.renderFont = pygame.font.Font(self.font, self.size)
        self.renderText = pygame.Surface.__new__(pygame.Surface)
        self.Text(self.text)
        self.rect = self.renderText.get_rect()
        self.rect.center = (self.rectTransform.position.x, self.rectTransform.position.y)
        texts.append(self)

    def Text(self, text):
        self.text = text
        self.updateText()

    def setSize(self, size):
        self.size = size
        self.updateText()

    def setTextColor(self, color):
        self.textColor = color
        self.updateText()

    def setTextColour(self, color):
        self.textColor = color
        self.updateText()

    def setBGColor(self, color):
        self.BGColor = color
        self.updateText()

    def setBGColour(self, color):
        self.BGColor = color
        self.updateText()

    def updateText(self):
        self.renderFont = pygame.font.Font(self.font, self.size)
        self.renderText = self.renderFont.render(str(self.text), True,
                                                 self.textColor.toTuple(),
                                                 self.BGColor.toTuple())


class RectTransform:
    def __init__(self, pos, angle):
        self.position = pos
        self.angle = angle
        self.text = None

    def setPos(self, pos):
        self.position = pos
        self.text.rect.center = (self.position.x, self.position.y)

    def translate(self, translation):
        self.setPos(self.position + translation)

    def setRot(self, angle):
        self.angle = angle % 360

    def rotate(self, angle):
        self.angle = (self.angle + angle) % 360


def init():
    pygame.init()


init()


class Window:
    def __init__(self, *args):  # (self, Width, Height, title, icon):
        self.running = True
        if len(args) == 4:
            self.__init__(args[0], args[1], args[2])
            self.icon = pygame.image.load(str(args[3]))
            self.setIcon(str(args[3]))
        elif len(args) == 3:
            self.width = int(args[0])
            self.height = int(args[1])
            self.screen = pygame.display.set_mode((self.width, self.height))
            self.title = str(args[2])
            self.setTitle(self.title)
        elif len(args) == 2:
            self.__init__(args[0], args[1], "Game Window")
        else:
            raise TypeError("Window() takes from 2 to 4 positional arguments, but  " + str(len(args)) + " were given")
        self.bgColor = Colors.white
        Input.Update()

    def fillBG(self, color):
        if self.running:
            self.screen.fill(color.toTuple())

    def setBG(self, color):
        self.bgColor = color

    def setTitle(self, title):
        self.title = title
        pygame.display.set_caption(title)

    def setIcon(self, icon):
        self.icon = pygame.image.load(icon)
        pygame.display.set_icon(self.icon)

    def Update(self):
        global debug
        if self.running:
            if Input.GetEvent(QUIT):
                self.Quit()
                return

            self.fillBG(self.bgColor)

            for txt in texts:
                txt.Text(txt.text)
                size = pygame.transform.rotate(txt.renderText, txt.rectTransform.angle).get_rect().size
                self.screen.blit(pygame.transform.rotate(txt.renderText, -txt.rectTransform.angle),
                                 (int(txt.rectTransform.position.x) - int(size[0] / 2),
                                  int(txt.rectTransform.position.y) - int(size[1] / 2)))

            for obj in objects:
                size = pygame.transform.rotate(obj.Img, obj.transform.angle).get_rect().size
                self.screen.blit(pygame.transform.rotate(obj.Img, -obj.transform.angle),
                                 (int(obj.transform.position.x) - int(size[0] / 2),
                                  int(obj.transform.position.y) - int(size[1] / 2)))
            for key in lambdas:
                lambdas[key](self.screen, key)

            for func in debug:
                func(self.screen)

            debug = []

            Input.Update()
            pygame.display.update()
            RealTime.waitForRealTime(RealTime.deltaTime)

    def Quit(self):
        self.running = False
        pygame.quit()


# colors

keys = []
oldKeys = []
events = []


class Input:
    @staticmethod
    def GetKey(key):
        return keys[key]

    @staticmethod
    def GetKeyDown(key):
        return (not oldKeys[key]) and keys[key]

    @staticmethod
    def GetKeyUp(key):
        return oldKeys[key] and not keys[key]

    @staticmethod
    def GetEvent(event, attribute: str = "", value=None):
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
    def GetEventProperty(event, prop: str):
        for ev in events:
            if ev.type == event:
                return getattr(ev, prop)
        raise Exception(f"Event '{event}' doesn't exist. Maybe doesn't happen every frame?")

    # Mouse
    @staticmethod
    def MouseButtonDown(button):
        return Input.GetEvent(MOUSEBUTTONDOWN, "button", button)

    @staticmethod
    def MouseButtonUp(button):
        return Input.GetEvent(MOUSEBUTTONUP, "button", button)

    @staticmethod
    def MousePosition():
        pos = pygame.mouse.get_pos()
        return Vector2(pos[0], pos[1])

    @staticmethod
    def Update():
        global keys, events, oldKeys
        oldKeys = keys
        keys = pygame.key.get_pressed()
        events = pygame.event.get()


class Mathf:
    @staticmethod
    def Clamp(value, Min, Max):
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
    def setDT(dt):
        RealTime.deltaTime = dt

    @staticmethod
    def waitForRealTime(dt):
        RealTime.t = RealTime.t + dt
        wait = RealTime.t - time.monotonic()
        if wait > 0:
            time.sleep(wait)
