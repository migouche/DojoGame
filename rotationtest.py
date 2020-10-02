from pygamemig import *

window = Window(800, 600)

pac = Object("py.png", Vector2(100, 100))
pac.transform.setPos(Vector2(400, 400))

while window.running:
    pac.transform.rotate(.1)
    window.fillBG(white)
    window.Update()
