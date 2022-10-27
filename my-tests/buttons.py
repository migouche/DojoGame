from dojogame import *
from pygame.constants import *

window = Window(400, 400, flags=RESIZABLE)

polygon = Collider.add_collider(Polygon.Square(100, color=Colors.red))
button = Button(polygon, Text("freesansbold.ttf", 30, Colors.black, "haha"))
button.transform.set_position(Vector2(200, 200))


@button.on_click
def button_on_click():
    print("clicked")


while window.running:
    if Input.get_key_down(K_ESCAPE) or Input.get_key_down(K_q):
        window.quit()
    window.update()
