from pygamemig import *

window = Window(800, 800)

pac = Object("pacman.png", Vector2(200, 100))
pac.transform.setPos(Vector2(400, 400))

txt = Text("freesansbold.ttf", 30, Colors.black, Colours.white)
txt.Text("wtf")
txt.rectTransform.setPos(Vector2(100, 100))

window.setBG(Colors.red)

print(RealTime.deltaTime)
print(Vector2.angleDeg(Vector2(0, 10), Vector2(1, 0)))

square = Square(40, color=Colors.purple)
square.rigidbody.position = Vector2(200, 200)
square.rigidbody.angle = -20

point = Circle(10, color=Colors.purple)
point.rigidbody.position = Vector2(300, 250)

fsquare = Square(40, color=Colors.black)
fsquare.rigidbody.position = square.rigidbody.position

while window.running:

    Lines.drawRay(Input.MousePosition(), Vector2(-1, -1), 350)

    hit = Raycast.raycast(Input.MousePosition(), Vector2(-1, -1), 350)

    if hit:
        Lines.drawRay(hit.point, hit.normal, 100)
    # print(hit.point)

    if Input.GetKeyUp(K_SPACE):
        print("up")
    pac.transform.rotate(30 * RealTime.deltaTime)
    txt.rectTransform.rotate(30 * RealTime.deltaTime)
    pac.transform.position = Input.MousePosition()

    if Input.MouseButtonUp(1):
        print("yeet")

    # print(Input.MousePosition())
    # window.fillBG(white)
    window.Update()

    if Input.GetKey(K_q):
        window.Quit()
    # print(pygame.display.get_window_size())
