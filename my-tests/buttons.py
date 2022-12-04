from dojogame import *
from pygame.constants import *

game = DojoGame()

polygon = Collider.add_collider(Polygon.Square(100, color=Colors.red))
button = Button(polygon, Text("freesansbold.ttf", 30, Colors.black, "haha"))
button.transform.set_position(Vector2(200, 200))

sound = Sound("data/audio/270334__littlerobotsoundfactory__jingle-lose-01.wav")


@button.on_click
def button_on_click():
    sound.play()


def update():
    if Input.get_key_down(K_ESCAPE) or Input.get_key_down(K_q):
        game.quit()


game.run()
