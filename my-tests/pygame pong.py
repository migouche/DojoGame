import pygame
import math
import random


class Vector2:  # de 50 a 250
    def __init__(self, X, Y):
        self.x = X
        self.y = Y

    def __add__(self, v):
        return Vector2(self.x + v.x, self.y + v.y)

    def __sub__(self, v):
        return Vector2(self.x - v.x, self.y - v.y)

    def __mul__(self, f):
        return Vector2(self.x * f, self.y * f)

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


pygame.init()

size = Vector2(800, 600)

screen = pygame.display.set_mode((size.x, size.y))
pygame.display.set_caption("Pong")
pygame.display.set_icon(pygame.image.load("../examples/data/py.png"))


class Object:

    def __init__(self, Offset):
        self.offset = Offset
        self.pos = Vector2(size.x / 2, size.y / 2)
        self.delta = Vector2.zero()


class Ball(Object):
    def __init__(self, Size, Speed, Offset):
        super(Ball, self).__init__(Offset)
        self.size = Size
        self.Img = pygame.transform.scale(pygame.image.load("../examples/data/ball.png"), (self.size.x, self.size.y))
        self.defaultSpeed = Speed
        self.speed = self.defaultSpeed
        self.rect = self.Img.get_rect()
        self.angle = random.randint(-125, 125) / 100
        self.dir = Vector2(math.cos(self.angle), math.sin(self.angle))

    def resetPos(self):
        self.pos = Vector2(size.x / 2, size.y / 2)
        self.angle = random.randint(-125, 125) / 100
        self.dir = Vector2(math.cos(ball.angle), math.sin(ball.angle))
        self.speed = self.defaultSpeed

    def is_collided_with(self, obj):
        return self.rect.colliderect(obj.rect)


class Paddle(Object):
    def __init__(self, Pos, Size, Speed, Offset):
        super(Paddle, self).__init__(Offset)
        self.pos = Pos
        self.size = Size
        self.Img = pygame.transform.scale(pygame.image.load("../examples/data/pala.png"), (self.size.x, self.size.y))
        self.speed = Speed
        self.rect = self.Img.get_rect()

    def is_collided_with(self, obj):
        return self.rect.colliderect(obj.rect)


ball = Ball(Vector2(30, 30), 0.25, Vector2(20, 20))

lPaddle = Paddle(Vector2(0, size.y / 2), Vector2(30, 200), 0.5, Vector2(15, 100))
rPaddle = Paddle(Vector2(size.x, size.y / 2), Vector2(30, 200), 0.5, Vector2(15, 100))

objects = [ball, lPaddle, rPaddle]


def drawObjects():
    for obj in objects:
        screen.blit(obj.Img, (int(obj.pos.x) - obj.offset.x, int(obj.pos.y) - obj.offset.y))
        obj.delta = Vector2.zero()


scoreRight = scoreLeft = 0
Lfont = pygame.font.Font('freesansbold.ttf', 40)
scoreLeftTxt = Lfont.render(str(scoreLeft), True, (0, 0, 0), (255, 255, 255))
scoreLeftRect = scoreLeftTxt.get_rect()
scoreLeftRect.center = (int(size.x / 2) - 200, 50)

Rfont = pygame.font.Font('freesansbold.ttf', 40)
scoreRightTxt = Rfont.render(str(scoreRight), True, (0, 0, 0), (255, 255, 255))
scoreRightRect = scoreRightTxt.get_rect()
scoreRightRect.center = (int(size.x / 2) + 200, 50)


def drawUI():
    screen.blit(scoreLeftTxt, scoreLeftRect)
    screen.blit(scoreRightTxt, scoreRightRect)


def updateUI():
    global Lfont, scoreLeftTxt, scoreLeftRect, scoreRightRect, Rfont, scoreRightTxt, scoreRightRect
    Lfont = pygame.font.Font('freesansbold.ttf', 40)
    scoreLeftTxt = Lfont.render(str(scoreLeft), True, (0, 0, 0), (255, 255, 255))
    scoreLeftRect = scoreLeftTxt.get_rect()
    scoreLeftRect.center = (int(size.x / 2) - 200, 50)

    Rfont = pygame.font.Font('freesansbold.ttf', 40)
    scoreRightTxt = Rfont.render(str(scoreRight), True, (0, 0, 0), (255, 255, 255))
    scoreRightRect = scoreRightTxt.get_rect()
    scoreRightRect.center = (int(size.x / 2) + 200, 50)


def moveObjects():
    for obj in objects:
        obj.pos += obj.delta * obj.speed
        obj.pos.x = Clamp(obj.pos.x, 0, size.x)
        obj.pos.y = Clamp(obj.pos.y, 0, size.y)


def Clamp(v, m, M):
    if v >= M:
        return M
    elif v <= m:
        return m
    else:
        return v


def lose():
    global can_start
    ball.resetPos()
    canStart = False


running = True

can_start = False

while running:
    if Vector2.distance(ball.pos, Vector2(size.x, ball.pos.y)) <= 20.0:
        if Vector2.distance(ball.pos, rPaddle.pos) <= 100:

            ball.angle = random.randint(175, 280) / 100
            ball.dir = Vector2(math.cos(ball.angle), math.sin(ball.angle))
            ball.speed += 0.05
        else:
            lose()
            scoreLeft += 1
            updateUI()

    if Vector2.distance(ball.pos, Vector2(0, ball.pos.y)) <= 20.0:
        if Vector2.distance(ball.pos, lPaddle.pos) <= 100:
            ball.angle = random.randint(-125, 125) / 100
            ball.dir = Vector2(math.cos(ball.angle), math.sin(ball.angle))
            ball.speed += 0.05
        else:
            lose()
            scoreRight += 1
            updateUI()

    if Vector2.distance(ball.pos, Vector2(ball.pos.x, size.y)) <= 20:
        ball.dir.y *= -1

    if Vector2.distance(ball.pos, Vector2(ball.pos.x, 0)) <= 20:
        ball.dir.y *= -1

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        rPaddle.delta.y -= 1
    if keys[pygame.K_DOWN]:
        rPaddle.delta.y += 1
    if keys[pygame.K_w]:
        lPaddle.delta.y -= 1
    if keys[pygame.K_s]:
        lPaddle.delta.y += 1

    can_start = can_start or keys[pygame.K_SPACE]

    if can_start:
        ball.delta = ball.dir
    else:
        ball.delta = Vector2.zero()

    screen.fill((255, 255, 255))

    moveObjects()

    drawObjects()
    drawUI()

    pygame.display.update()

pygame.quit()
