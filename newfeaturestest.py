from pygamemig import *

window = Window(800, 1000)

pac = Object("pacman.png", Vector2(200, 100))
pac.transform.setPos(Vector2(400, 400))

txt = Text("freesansbold.ttf", 30, Colors.black, Colours.white)
txt.Text("wtf")
txt.rectTransform.setPos(Vector2(100, 100))

window.setBG(Colors.purple)

print(RealTime.deltaTime)
print(Vector2.angleDeg(Vector2(0,10), Vector2(1, 0)))

polygon = Object.regularPolygon(5, Vector2(150, 150))
polygon.transform.setPos(Vector2(window.width/2, window.height/2))

while window.running:
    if Input.GetKey(K_q):
        window.Quit()
    if Input.GetKeyUp(K_SPACE):
        print("up")
    pac.transform.rotate(30 * RealTime.deltaTime)
    txt.rectTransform.rotate(30 * RealTime.deltaTime)

    if Input.GetMouseButtonUp(1):
        print("yeet")
    #window.fillBG(white)
    window.Update()
