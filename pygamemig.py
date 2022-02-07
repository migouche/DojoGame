import pygame
from pygame.constants import *
import math
import random
import time


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

    @staticmethod
    def distance(_from, _to):
        return (_to - _from).magnitude()

    @staticmethod
    def distance(a, b):
        return (b - a).magnitude()

    def normalized(self):
        return self / self.magnitude()

    @staticmethod
    def fromAngle(angle):
        return Vector2(math.cos(angle), math.sin(angle))

    @staticmethod
    def random():
        return Vector2.radRandom(0, 6.28)

    @staticmethod
    def degRandom(a, b):
        return Vector2.radRandom(a * Mathf.Deg2Rad, b * Mathf.Deg2Rad)

    @staticmethod
    def radRandom(a, b):
        return Vector2.fromAngle(random.randint(int(a * 100), int(b * 100)) / 100).normalized()


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
    def regularPolygon(cls, sides, scale):
        self = cls.__new__(cls)
        self.transform = Transform(Vector2.zero(), 0, scale)
        self.transform.object = self
        self.Img = pygame.Surface((self.transform.scale.x, self.transform.scale.y))
        self.rect = pygame.draw.lines(self.Img, (255, 255, 255), True, [(0, 0), (1, 0), (1, 1), (0, 1)])
        return self


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
        self.renderText = None
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
                                                 (self.textColor.red, self.textColor.green, self.textColor.blue),
                                                 (self.BGColor.red, self.BGColor.green, self.BGColor.blue))


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
            self.screen.fill((color.red, color.green, color.blue))

    def setBG(self, color):
        self.bgColor = color

    def setTitle(self, title):
        self.title = title
        pygame.display.set_caption(title)

    def setIcon(self, icon):
        self.icon = pygame.image.load(icon)
        pygame.display.set_icon(self.icon)

    def Update(self):
        if self.running:
            for event in Input.Events():
                if event.type == QUIT:
                    self.Quit()
                    return

            self.fillBG(self.bgColor)

            for txt in texts:
                txt.Text(txt.text)
                size = pygame.transform.rotate(txt.renderText, txt.rectTransform.angle).get_rect().size
                self.screen.blit(pygame.transform.rotate(txt.renderText, txt.rectTransform.angle),
                                 (int(txt.rectTransform.position.x) - int(size[0] / 2),
                                  int(txt.rectTransform.position.y) - int(size[1] / 2)))

            for obj in objects:
                size = pygame.transform.rotate(obj.Img, obj.transform.angle).get_rect().size
                self.screen.blit(pygame.transform.rotate(obj.Img, obj.transform.angle),
                                 (int(obj.transform.position.x) - int(size[0] / 2),
                                  int(obj.transform.position.y) - int(size[1] / 2)))

            Input.Update()
            pygame.display.update()
            RealTime.waitForRealTime(RealTime.deltaTime)

    def Quit(self):
        self.running = False
        pygame.quit()


class Color:
    def __init__(self, r, g, b):
        self.red = r
        self.green = g
        self.blue = b

    @staticmethod
    def fromHex(h):
        c = tuple(int(h.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
        return Color(c[0], c[1], c[2])


class Colors:
    white = Color(255, 255, 255)
    black = Color(0, 0, 0)
    red = Color(255, 0, 0)
    green = Color(0, 255, 0)
    blue = Color(0, 0, 255)


Colour = Color
Colours = Colors
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
    def GetEvent(event):
        b = False
        for ev in pygame.event.get():
            if ev.type == event:
                b = True
        return b

    @staticmethod
    def Events():
        return pygame.event.get()

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
