from dojogame.dojogame import *

window = Window(800, 600)

pac = Object("data/pacman.png", Vector2(100, 50))
pac.transform.set_pos(Vector2(window.width / 2, window.height / 2))

py = Object("data/py.png", Vector2(50, 50))
py.transform.set_pos(Vector2(window.width / 2, 100))

while window.running:

    if Input.get_key(K_UP):
        pac.transform.translate(Vector2(0, -.2))

    if Input.get_key(K_DOWN):
        pac.transform.translate((Vector2(0, .2)))

    pacRect = pac.Img.get_rect()
    pacRect.center = (int(pac.transform.position.x), int(pac.transform.position.y))

    pyRect = py.Img.get_rect()
    pyRect.center = (int(py.transform.position.x), int(pac.transform.position.y))

    if pyRect.colliderect(pacRect):
        print("yeet")
    window.fill_bg(Colors.red)
    window.update()
