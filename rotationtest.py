from pygamemig import *

window = Window(800, 600)

pac = Object("pacman.png", Vector2(200, 100))
pac.transform.setPos(Vector2(400, 400))

while window.running:
    pac.transform.rotate(.1)
    print(pac.transform.angle)
    window.fillBG(white)
    window.Update()
