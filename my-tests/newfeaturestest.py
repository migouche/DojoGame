from dojogame import *
from dojogame.dojoconstants import *

from pygame.constants import *

window = Window(400, 400, flags=RESIZABLE)
window.set_bg(Color.from_hex("ff00ff"))


txt = Text("freesansbold.ttf", 30, Color(0, 0, 0, 100))
txt.transform.set_position(Vector2(100, 100))


point2 = Circle(10)
point2.transform.position = Vector2(300, 250)
pos = point2.transform.position

point = Circle(10, color=Colors.purple)
point.transform.set_position(Vector2(300, 250))
Collider.add_collider(point)

rec2 = Polygon.Rectangle(200, 100, color=Color(255, 5, 5))
rec2.transform.set_position(Vector2(400, 400))
rec2.transform.set_rotation(45)

pac = Sprite("data/pacman.png", Vector2(200, 100), parent=rec2.transform)
pac.transform.set_position(Vector2(400, 400))
player = Polygon.Square(10)
Rigidbody.add_rigidbody(player)
_dir = Vector2(0, -1)

print(player.rigidbody)

lastCircle = Circle(radius=5, color=Colors.white)  # should be and is in the middle
lastCircle.transform.set_position(Vector2(window.width / 2 + 50, window.height / 2 + 50))

player.transform.set_rotation(10)

triangle = Polygon([Vector2(0, 0), Vector2(100, 0), Vector2(50, 100)], color=Colors.red, width=0)
triangle.transform.set_position(Vector2(window.width / 2, window.height / 2))
Collider.add_collider(triangle)

triangle2 = Polygon([Vector2(0, 0), Vector2(100, 0), Vector2(50, 100)], color=Colors.red, width=5)
triangle2.transform.set_position(Vector2(window.width / 2 + 50, window.height / 2 + 50))
Collider.add_collider(triangle2)


child = Polygon.Square(10, color=Colors.blue)
child.transform.set_parent(triangle2.transform)
child.transform.set_position(Vector2(50, 50))

square = Polygon.Square(40, color=Color(100, 0, 255, 100))
square.transform.set_position(Vector2(200, 200))
square.transform.set_local_scale(Vector2(1, 2))

Collider.add_collider(square)
print(square.collider.aabb)
RealTime.set_framerate(75)

while window.running:
    txt.text = f"FPS: {int(RealTime.clock.get_fps())}"
    triangle.transform.rotate(RealTime.delta_time * 10)
    triangle2.transform.rotate(-RealTime.delta_time * 10)

    Lines.draw_axis_aligned_bounding_box(triangle.collider)
    Lines.draw_axis_aligned_bounding_box(triangle2.collider)

    triangle.color = triangle2.color = Colors.red if triangle.collider\
        .collide_with(triangle2.collider) else Colors.blue

    # triangle.color = triangle2.color = Colors.red if Collisions.gjk(triangle, triangle2) else Colors.blue

    if Input.get_mouse_button_down(1):
        _dir.y *= -1
    Lines.draw_ray(Input.get_mouse_position(), _dir, 350)
    square.transform.rotate(100 * RealTime.delta_time)

    if hit := Raycast.raycast_polygon(Input.get_mouse_position(), _dir, square.collider, 400):
        Lines.draw_ray(hit.point, hit.normal, 100)

    # print(hit.point)

    if Input.get_key_up(K_SPACE):
        print("up")
    pac.transform.rotate(30 * RealTime.delta_time)
    txt.transform.rotate(30 * RealTime.delta_time)
    pac.transform.set_position(Input.get_mouse_position(), space=Space.World)

    if Input.get_key(K_a):
        player.rigidbody.add_force_at_position(Vector2(-30, 0), player.transform.position)
    if Input.get_key(K_d):
        player.rigidbody.add_force_at_position(Vector2(30, 0), player.transform.position)
    if Input.get_key(K_w):
        player.rigidbody.add_force_at_position(Vector2(0, -30), player.transform.position + Vector2(1, 0))
    if Input.get_key(K_s):
        player.rigidbody.add_force_at_position(Vector2(0, 30), player.transform.position, space=Space.Self)

    if Input.get_mouse_button_down(MOUSE_BUTTON_LEFT):
        pac.transform.set_local_scale(2 * pac.transform.local_scale)
        if Collisions.point_inside_polygon(Input.get_mouse_position(), square.collider):
            print("inside")

    if Input.get_mouse_button_down(MOUSE_BUTTON_RIGHT):
        pac.transform.set_local_scale(pac.transform.local_scale / 2)

    if Input.get_mouse_button_down(MOUSE_SCROLL_UP):
        pac.transform.set_local_scale(Vector2(pac.transform.local_scale.x, pac.transform.local_scale.y * 2))

    if Input.get_mouse_button_down(MOUSE_SCROLL_DOWN):
        pac.transform.set_local_scale(Vector2(pac.transform.local_scale.x, pac.transform.local_scale.y / 2))

    window.update()

    if Input.get_key_down(K_q):
        window.quit()
