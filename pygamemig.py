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

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    @staticmethod
    def distance(a, b):
        return (b - a).magnitude()

    def normalized(self):
        return self / self.magnitude()

    @staticmethod
    def fromAngle(angle):
        return Vector2(math.cos(angle), math.sin(angle))

    @staticmethod
    def Random():
        return Vector2(math.cos(random.randint(0, 628) / 100), math.sin(random.randint(0, 628) / 100)).normalized()

    @staticmethod
    def DegRandom(a, b):
        angle = random.randint(int(a * 100 * Deg2Rad), int(b * 100 * Deg2Rad)) / 100
        return Vector2(math.cos(angle), math.sin(angle))

    @staticmethod
    def RadRandom(a, b):
        angle = random.randint(int(a * 100), int(b * 100)) / 100
        return Vector2(math.cos(angle), math.sin(angle))


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

    @staticmethod
    def Random():
        return Vector2Int.DegRandom(0, 360)

    @staticmethod
    def DegRandom(a, b):
        angle = random.randint(int(a * 100 * Deg2Rad), int(b * 100 * Deg2Rad)) / 100
        return Vector2Int(math.cos(angle), math.sin(angle))

    @staticmethod
    def RadRandom(a, b):
        angle = random.randint(int(a * 100), int(b * 100)) / 100
        return Vector2Int(math.cos(angle), math.sin(angle))


objects = []
texts = []


class Object:
    def __init__(self, img, scale):
        # self.transform = transform
        self.transform = Transform(Vector2.zero(), 0, scale)
        self.transform.object = self
        self.Img = pygame.transform.scale(pygame.image.load(img), (self.transform.scale.x, self.transform.scale.y))

        self.offset = scale / 2
        objects.append(self)


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
        Input.Update()

    def fillBG(self, color):
        if self.running:
            self.screen.fill((color.red, color.green, color.blue))

    def setTitle(self, title):
        self.title = title
        pygame.display.set_caption(title)

    def setIcon(self, icon):
        self.icon = pygame.image.load(icon)
        pygame.display.set_icon(self.icon)

    def Update(self):
        if self.running:
            for obj in objects:
                self.screen.blit(pygame.transform.rotate(obj.Img, obj.transform.angle),
                                 (int(obj.transform.position.x) - int(obj.offset.x),
                                  int(obj.transform.position.y) - int(obj.offset.y)))
            for txt in texts:
                txt.Text(txt.text)
                self.screen.blit(txt.renderText, txt.rect)

            Input.Update()
            pygame.display.update()

            for event in Input.Events():
                if event.type == QUIT:
                    self.Quit()

    def Quit(self):
        self.running = False
        pygame.quit()


class Color:
    def __init__(self, r, g, b):
        self.red = r
        self.green = g
        self.blue = b


Colour = Color
# colors:
white = Color(255, 255, 255)
black = Color(0, 0, 0)
red = Color(255, 0, 0)
green = Color(0, 255, 0)
blue = Color(0, 0, 255)

keys = []
events = []


class Input:
    @staticmethod
    def GetKey(key):
        return keys[key]

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
        global keys, events
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

    @staticmethod
    def waitForRealTime(dt):
        RealTime.t = RealTime.t + dt
        wait = RealTime.t - time.monotonic()
        if wait > 0:
            time.sleep(wait)
