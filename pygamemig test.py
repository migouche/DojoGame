from pygamemig import *

canStart = False

window = Window(800, 600, "pong", "py.png")

ball = Object("ball.png", Vector2(30, 30))


RightPaddle = Object("pala.png", Vector2(30, 200))

LeftPaddle = Object("pala.png", Vector2(30, 200))

LeftScore = RightScore = 0

# RightText = Text(Vector2((window.width / 2) + 200, 50), RightScore, 30, "freesansbold.ttf", black, white)
RightText = Text("freesansbold.ttf", 30, Colors.black, Colors.white)
RightText.rectTransform.setPos(Vector2(window.width / 2 + 200, 50))
RightText.Text(0)

# LeftText = Text(Vector2((window.width / 2) - 200, 50), LeftScore, 30, "freesansbold.ttf", black, white)
LeftText = Text("freesansbold.ttf", 30, Colors.black, Colors.white)
LeftText.rectTransform.setPos(Vector2(window.width / 2 - 200, 50))
LeftText.Text(0)

paddleSpeed = 500
ballSpeed = 250
ballDir = Vector2.random()


def ResetPos():
    global ballDir, ballSpeed
    ball.transform.position = Vector2(window.width / 2, window.height / 2)
    RightPaddle.transform.setPos(Vector2(window.width, window.height / 2))
    LeftPaddle.transform.setPos(Vector2(0, window.height / 2))
    RightText.Text(RightScore)
    LeftText.Text(LeftScore)
    ballDir = Vector2.random()
    ballSpeed = 250


def lose():
    global canStart
    canStart = False
    ResetPos()


ResetPos()

while window.running:
    if Input.GetKey(K_UP):
        RightPaddle.transform.translate(Vector2(0, -1) * paddleSpeed * RealTime.deltaTime)
    if Input.GetKey(K_DOWN):
        RightPaddle.transform.translate(Vector2(0, 1) * paddleSpeed * RealTime.deltaTime)
    if Input.GetKey(K_w):
        LeftPaddle.transform.translate(Vector2(0, -1) * paddleSpeed * RealTime.deltaTime)
    if Input.GetKey(K_s):
        LeftPaddle.transform.translate(Vector2(0, 1) * paddleSpeed * RealTime.deltaTime)
    if Input.GetKey(K_e):
        # ball.transform.setScale(ball.transform.scale + Vector2(5, 5))
        # RightText.setTextColor(red)
        # RightText.rectTransform.setPos(Vector2(50, 50))
        # RightText.rectTransform.translate(Vector2(-1, 0))
        pass
    if Input.GetKey(K_q):
        window.Quit()

    if Vector2.distance(ball.transform.position, Vector2(window.width, ball.transform.position.y)) <= 20.0:
        if Vector2.distance(ball.transform.position, RightPaddle.transform.position) <= 110:
            ballDir = Vector2.degRandom(135, 225)
            ballSpeed += 50
        else:
            LeftScore += 1
            lose()

    if Vector2.distance(ball.transform.position, Vector2(0, ball.transform.position.y)) <= 20.0:
        if Vector2.distance(ball.transform.position, LeftPaddle.transform.position) <= 110:
            ballDir = Vector2.degRandom(-45, 45)
            ballSpeed += 50
        else:
            RightScore += 1
            lose()

    canStart = canStart or Input.GetKey(K_SPACE)

    if canStart:
        ball.transform.translate(ballDir * ballSpeed * RealTime.deltaTime)

    if Vector2.distance(ball.transform.position, Vector2(ball.transform.position.x, window.height)) <= 20:
        ballDir.y *= -1

    if Vector2.distance(ball.transform.position, Vector2(ball.transform.position.x, 0)) <= 30:
        ballDir.y *= -1
    RightPaddle.transform.position.y = Mathf.Clamp(RightPaddle.transform.position.y, 0, window.height)
    LeftPaddle.transform.position.y = Mathf.Clamp(LeftPaddle.transform.position.y, 0, window.height)

    window.Update()
