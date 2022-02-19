from pygamemig import *

window = Window(800, 800)

pac = Object("pacman.png", Vector2(200, 100))
pac.transform.setPos(Vector2(400, 400))

txt = Text("freesansbold.ttf", 30, Colors.black, Color(255, 255, 255, 0))
txt.Text("wtf")
txt.rectTransform.setPos(Vector2(100, 100))

window.setBG(Colors.red)

print(RealTime.deltaTime)
print(Vector2.angleDeg(Vector2(0, 10), Vector2(1, 0)))

square = Square(40, color=Colors.purple)
square.rigidbody.position = Vector2(200, 200)

point2 = Circle(10)
point2.rigidbody.position = Vector2(300, 250)
point2.rigidbody.rotateAroundOrigin(90, square.rigidbody.position)

point = Circle(10, color=Colors.purple)
point.rigidbody.position = Vector2(300, 250)

rec = Rectangle(200, 100)
rec.rigidbody.position = Vector2(400, 400)
rec.rigidbody.angle = 45

_dir = Vector2(0, -1)
while window.running:
    if Input.MouseButtonDown(1):
        _dir.y *= -1
    Lines.drawRay(Input.MousePosition(), _dir, 350)
    square.rigidbody.rotate(3)

    hit = Raycast.raycast(Input.MousePosition(), _dir, 350)

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

    if Input.GetKeyDown(K_q):
        window.Quit()
    # print(pygame.display.get_window_size())
