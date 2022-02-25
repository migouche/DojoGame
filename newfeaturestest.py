from pygamemig import *

window = Window(400, 400)
window.setBG(Color.fromHex("ff00ff"))

pac = Object("pacman.png", Vector2(200, 100))
pac.transform.setPos(Vector2(400, 400))

txt = Text("freesansbold.ttf", 30, Colors.black, Color(255, 255, 255, 0))
txt.Text("wtf")
txt.rectTransform.setPos(Vector2(100, 100))

print(RealTime.deltaTime)
print(Vector2.angleDeg(Vector2(0, 10), Vector2(1, 0)))

square = Square(40, color=Colors.purple)
square.transform.position = Vector2(200, 200)

point2 = Circle(10)
point2.transform.position = Vector2(300, 250)
point2.transform.rotateAroundOrigin(90, square.transform.position)
pos = point2.transform.position

point = Circle(10, 4, color=Colors.purple)
point.transform.position = Vector2(300, 250)

rec = Rectangle(200, 100)
rec.transform.position = Vector2(400, 400)
rec.transform.rotation = 45

player = Circle(10)
_dir = Vector2(0, -1)

lastCircle = Circle(radius=5, color=Colors.white, position=rec.transform.position)  # should be and is in the middle

player.transform.rotation = 10

# RealTime.setDT(1/20)
while window.running:
    print(window.width, window.height)
    if Input.MouseButtonDown(1):
        _dir.y *= -1
    Lines.drawRay(Input.MousePosition(), _dir, 350)
    square.transform.rotate(3)

    if hit := Raycast.raycast(Input.MousePosition(), _dir, 350):
        Lines.drawRay(hit.point, hit.normal, 100)

    # print(hit.point)

    if Input.GetKeyUp(K_SPACE):
        print("up")
    pac.transform.rotate(30 * RealTime.deltaTime)
    txt.rectTransform.rotate(30 * RealTime.deltaTime)
    pac.transform.position = Input.MousePosition()

    if Input.GetKey(K_a):
        player.rigidbody.addForce(Vector2(-30, 0))
    if Input.GetKey(K_d):
        player.rigidbody.addForce(Vector2(30, 0))
    if Input.GetKey(K_w):
        player.rigidbody.addForce(Vector2(0, -30))
    if Input.GetKey(K_s):
        player.rigidbody.addForce(Vector2(0, 30))

    if Input.MouseButtonUp(1):
        print("yeet")

    # print(Input.MousePosition())
    # window.fillBG(white)
    window.Update()

    if Input.GetKeyDown(K_q):
        window.Quit()
    # print(pygame.display.get_window_size())
