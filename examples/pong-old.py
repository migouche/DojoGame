from dojogame import *
from pygame.constants import *

can_start = False

# window = Window(800, 600, "pong", "data/images/py.png")

game = DojoGame()
Collider.add_collider(ball := Circle(15, Colors.white))

Collider.add_collider(right_paddle := Polygon.Rectangle(30, 200, Colors.white))
Collider.add_collider(left_paddle := Polygon.Rectangle(30, 200, Colors.white))

left_score = right_score = 0

right_text = Text("freesansbold.ttf", 30, Colors.white)
right_text.set_text(0)

left_text = Text("freesansbold.ttf", 30, Colors.white)
left_text.set_text(0)

paddleSpeed = 500
ball_speed = 100
ball_dir = Vector2.random()


def reset_pos():
    global ball_dir, ball_speed
    ball.transform.set_position(Vector2(window.width / 2, window.height / 2))
    right_paddle.transform.set_position(Vector2(window.width, window.height / 2))
    left_paddle.transform.set_position(Vector2(0, window.height / 2))
    right_text.set_text(right_score)
    left_text.set_text(left_score)
    ball_dir = Vector2.random()
    ball_speed = 250


def lose():
    global can_start
    can_start = False
    reset_pos()


def pre_init():
    DojoGame.config_window(800, 600, "pong", "data/py.png", flags=0)


def start():
    global window
    window = game.window
    window.set_bg(Colors.black)
    right_text.transform.set_position(Vector2(window.width / 2 + 200, 50))
    left_text.transform.set_position(Vector2(window.width / 2 - 200, 50))
    reset_pos()


def update():
    if Input.get_key_down(K_ESCAPE):
        game.quit()
    global ball_dir, ball_speed, left_score, right_score, can_start

    if Input.get_key(K_UP):
        right_paddle.transform.translate(Vector2(0, -1) * paddleSpeed * RealTime.delta_time)
    if Input.get_key(K_DOWN):
        right_paddle.transform.translate(Vector2(0, 1) * paddleSpeed * RealTime.delta_time)
    if Input.get_key(K_w):
        left_paddle.transform.translate(Vector2(0, -1) * paddleSpeed * RealTime.delta_time)
    if Input.get_key(K_s):
        left_paddle.transform.translate(Vector2(0, 1) * paddleSpeed * RealTime.delta_time)

    if Input.get_key_down(K_q):
        game.quit()

    if ball.collider.collide_with(right_paddle.collider):
        ball_dir = Vector2.deg_random(135, 225)
        ball_speed += 50
    elif ball.transform.position.x >= window.width:
        left_score += 1
        lose()

    if ball.collider.collide_with(left_paddle.collider):
        ball_dir = Vector2.deg_random(-45, 45)
        ball_speed += 50
    elif ball.transform.position.x <= 0:
        right_score += 1
        lose()

    can_start = can_start or Input.get_key(K_SPACE)

    if ball.transform.position.y >= window.height - ball.radius or ball.transform.position.y <= ball.radius:
        ball_dir.y *= -1

    if can_start:
        ball.transform.translate(ball_dir * ball_speed * RealTime.delta_time)

    right_paddle.transform.position.y = Mathf.clamp(right_paddle.transform.position.y, 0, window.height)
    left_paddle.transform.position.y = Mathf.clamp(left_paddle.transform.position.y, 0, window.height)


game.run()
