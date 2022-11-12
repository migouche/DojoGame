from dojogame import *

window = Window(800, 600, "Collision Tests", flags=pygame.constants.RESIZABLE)

c1 = Collider.add_collider(Circle(150, Colors.red, 1))
c2 = Collider.add_collider(Circle(50, Colors.blue, 1))

p1 = Collider.add_collider(
    Polygon([Vector2(0, 0), Vector2(100, 0), Vector2(100, 50), Vector2(50, 100)], Colors.red, 0))
p1.transform.position = Vector2(400, 400)

c1.transform.set_position(Vector2(300, 300))

txt = Text("freesansbold.ttf", 20, Colors.black)
txt.transform.position = Vector2(100, 20)
txt2 = Text("freesansbold.ttf", 20, Colors.black)
txt2.transform.position = Vector2(100, 40)
while window.running:
    c2.transform.position = Input.get_mouse_position()

    col = c1.collider.collide_with(c2.collider)
    col2 = c2.collider.collide_with(p1.collider)

    txt.text = f"Collision: {bool(col) or bool(col2)}"
    txt2.text = f"Fps: {int(RealTime.clock.get_fps())}"
    for point in col.contacts:
        Lines.draw_circle(point.point, 5, Colors.black)

    if Input.get_key_down(pygame.constants.K_ESCAPE) or Input.get_key_down(pygame.constants.K_q):
        window.quit()

    window.update()
