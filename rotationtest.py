from pygamemig import *

window = Window(800, 1000)

pac = Object("pacman.png", Vector2(200, 100))
pac.transform.setPos(Vector2(400, 400))

txt = Text("freesansbold.ttf", 30, Colors.black, Colours.white)
txt.Text("wtf")
txt.rectTransform.setPos(Vector2(100, 100))

window.setBG(Color.fromHex("#ff0000"))

RealTime.setDT(1/30)
print(RealTime.deltaTime)

while window.running:
    pac.transform.rotate(30 * RealTime.deltaTime)
    txt.rectTransform.rotate(30 * RealTime.deltaTime)
    #window.fillBG(white)
    window.Update()
