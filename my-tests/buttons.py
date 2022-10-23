from dojogame import *
from pygame.constants import *

window = Window(400, 400, flags=RESIZABLE)

polygon = Polygon.Square(100, color=Colors.red)
button = Button(polygon, Text("freesansbold.ttf", 30, Colors.black, "haha"))
button.transform.position = Vector2(200, 200)

print(button.transform.get_position(Space.World))
print(button.background.transform.get_position(Space.Self))
print(button.background.transform.get_position(Space.World))
print(button.foreground.transform.get_position(Space.Self))
print(button.foreground.transform.get_position(Space.World))
while window.running:

    window.update()
