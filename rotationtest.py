from pygamemig import *

window = Window(800, 1000)

pac = Object("pacman.png", Vector2(200, 100))
pac.transform.setPos(Vector2(400, 400))

txt = Text("freesansbold.ttf", 30, black, white)
txt.Text("wtf")
txt.rectTransform.setPos(Vector2(100, 100))

while window.running:
    pac.transform.rotate(.1)
    txt.rectTransform.rotate(.1)
    window.fillBG(white)
    window.Update()
