from dojogame import *

window = Window(400, 400, flags=RESIZABLE)
window.set_bg(Color.from_hex("ff00ff"))

pac = Object("data/pacman.png", Vector2(200, 100))
pac.transform.set_pos(Vector2(400, 400))

txt = Text("freesansbold.ttf", 30, Colors.black, Color(255, 255, 255, 0))
txt.set_text("wtf")
txt.rectTransform.set_pos(Vector2(100, 100))

print(RealTime.delta_time)
print(Vector2.angle_deg(Vector2(0, 10), Vector2(1, 0)))

square = Square(40, color=Colors.purple)
square.transform.position = Vector2(200, 200)

point2 = Circle(10)
point2.transform.position = Vector2(300, 250)
point2.transform.rotate_around_origin(90, square.transform.position)
pos = point2.transform.position

point = Circle(10, 4, color=Colors.purple)
point.transform.position = Vector2(300, 250)

rec = Rectangle(200, 100)
rec.transform.position = Vector2(400, 400)
rec.transform.rotation = 45

player = Square(10)
_dir = Vector2(0, -1)

lastCircle = Circle(radius=5, color=Colors.white, position=rec.transform.position)  # should be and is in the middle

player.transform.rotation = 10

triangle = Polygon([Vector2(0, 0), Vector2(100, 0), Vector2(50, 100)], color=Colors.red, width=5)
triangle.transform.position = Vector2(window.width/2, window.height/2)

triangle2 = Polygon([Vector2(0, 0), Vector2(100, 0), Vector2(50, 100)], color=Colors.red, width=5)
triangle2.transform.position = Vector2(window.width/2 + 50, window.height/2 + 50)



# RealTime.setDT(1/20)
while window.running:
    triangle.transform.rotate(RealTime.delta_time * 10)
    triangle2.transform.rotate(-RealTime.delta_time * 10)

    Debug.draw_circle(triangle.collider.aabb.max_v, 5, Colors.white)
    Debug.draw_circle(triangle.collider.aabb.min_v, 5, Colors.white)

    Debug.draw_axis_aligned_bounding_box(triangle)
    Debug.draw_rectangle_vertices([Vector2(0, 0), Vector2(0, 100), Vector2(100, 100), Vector2(100, 0)], Colors.red, 5)
    #print(triangle.collider.collide_with(triangle2.collider))

    if Input.get_mouse_button_down(1):
        _dir.y *= -1
    Lines.draw_ray(Input.get_mouse_position(), _dir, 350)
    square.transform.rotate(3)

    if hit := Raycast.raycast(Input.get_mouse_position(), _dir, 350):
        Lines.draw_ray(hit.point, hit.normal, 100)
        #print(player == hit.collider.object)


    # print(hit.point)

    if Input.get_key_up(K_SPACE):
        print("up")
    pac.transform.rotate(30 * RealTime.delta_time)
    txt.rectTransform.rotate(30 * RealTime.delta_time)
    pac.transform.position = Input.get_mouse_position()

    if Input.get_key(K_a):
        player.rigidbody.add_force_at_position(Vector2(-30, 0), player.transform.position)
    if Input.get_key(K_d):
        player.rigidbody.add_force_at_position(Vector2(30, 0), player.transform.position)
    if Input.get_key(K_w):
        player.rigidbody.add_force_at_position(Vector2(0, -30), player.transform.position + Vector2(1, 0))
    if Input.get_key(K_s):
        player.rigidbody.add_force_at_position(Vector2(0, 30), player.transform.position, space=Space.Self)

    if Input.get_mouse_button_down(1):
        print("yeet")

    # print(Input.MousePosition())
    # window.fillBG(white)
    window.update()

    if Input.get_key_down(K_q):
        window.quit()
    # print(pygame.display.get_window_size())
