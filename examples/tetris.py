from dojogame import *
from pygame.constants import *
"""doesnt work yet and is not finished, but im moving to other stuff for now :)"""
game = DojoGame()


# using tetris grand master rotation system
# drawing them correctly, later inverting y pos
pieces = [[[Vector2(0, -2), Vector2(0, -1), Vector2(0, 0), Vector2(0, 1)],  # I
           [Vector2(-2, 0), Vector2(-1, 0), Vector2(0, 0), Vector2(1, 0)],
           [Vector2(0, -2), Vector2(0, -1), Vector2(0, 0), Vector2(0, 1)],
           [Vector2(-2, 0), Vector2(-1, 0), Vector2(0, 0), Vector2(1, 0)]],

          [[Vector2(-1, 0), Vector2(0, 0), Vector2(0, 1), Vector2(1, 1)],  # S
           [Vector2(-1, 1), Vector2(-1, 0), Vector2(0, 0), Vector2(0, -1)],
           [Vector2(-1, 0), Vector2(0, 0), Vector2(0, 1), Vector2(1, 1)],
           [Vector2(-1, 1), Vector2(-1, 0), Vector2(0, 0), Vector2(0, -1)]
           ],

          [[Vector2(-1, 0), Vector2(0, 0), Vector2(0, -1), Vector2(1, -1)],  # Z
           [Vector2(-1, -1), Vector2(-1, 0), Vector2(0, 0), Vector2(0, 1)],
           [Vector2(-1, 0), Vector2(0, 0), Vector2(0, -1), Vector2(1, -1)],
           [Vector2(-1, -1), Vector2(-1, 0), Vector2(0, 0), Vector2(0, 1)]
           ],

          [[Vector2(-1, 0), Vector2(0, 0), Vector2(0, -1), Vector2(1, 0)],  # T
           [Vector2(-1, 0), Vector2(0, 1), Vector2(0, 0), Vector2(0, -1)],
           [Vector2(-1, 0), Vector2(0, 0), Vector2(0, 1), Vector2(1, 0)],
           [Vector2(1, 0), Vector2(0, 1), Vector2(0, 0), Vector2(0, -1)]
           ],

          [[Vector2(0, 0), Vector2(0, 1), Vector2(1, 0), Vector2(1, 1)],  # O
           [Vector2(0, 0), Vector2(0, 1), Vector2(1, 0), Vector2(1, 1)],
           [Vector2(0, 0), Vector2(0, 1), Vector2(1, 0), Vector2(1, 1)],
           [Vector2(0, 0), Vector2(0, 1), Vector2(1, 0), Vector2(1, 1)]
           ],

          [[Vector2(0, 1), Vector2(0, 0), Vector2(0, -1), Vector2(-1, -1)],  # J
           [Vector2(-1, 1), Vector2(-1, 0), Vector2(0, 0), Vector2(1, 0)],
           [Vector2(0, 1), Vector2(0, 0), Vector2(0, -1), Vector2(1, 1)],
           [Vector2(-1, 0), Vector2(0, 0), Vector2(1, 0), Vector2(1, -1)]
           ],

          [[Vector2(0, 1), Vector2(0, 0), Vector2(0, -1), Vector2(1, -1)],  # L
           [Vector2(-1, -1), Vector2(-1, 0), Vector2(0, 0), Vector2(1, 0)],
           [Vector2(0, 1), Vector2(0, 0), Vector2(0, -1), Vector2(-1, 1)],
           [Vector2(-1, 0), Vector2(0, 0), Vector2(1, 0), Vector2(1, 1)]
           ]]  # all pieces for all rotations


def draw_square(pos: Vector2, size: int, color: Color = Colors.black): # TODO: add to dojogame :)
    vertex1, vertex2, vertex3, vertex4 =\
        pos, pos + Vector2(size, 0), pos + Vector2(size, size), pos + Vector2(0, size)
    Lines.draw_rectangle([vertex1, vertex2, vertex3, vertex4], color)


SIZE = 30

board = [[True for _ in range(10)] for _ in range(20)]
print(board)
board[0][0] = True
print(board)

class Tetromino:
    def __init__(self, _type: int):
        self.rotation = 0
        self.type = _type
        self.pos = Vector2(0, 0)

    def rotate(self):
        self.rotation = (self.rotation + 1) % 4

    def draw(self):
        for i in range(4):
            pos = self.pos + Vector2(pieces[self.type][self.rotation][i].x * SIZE,
                                     -pieces[self.type][self.rotation][i].y * SIZE)
            draw_square(pos, SIZE, Colors.red)

    def try_go_down(self):
        global board
        for i in range(4):
            pass






def config():
    DojoGame.config_window(400, 800, "Tetris", flags=RESIZABLE)


piece = Tetromino(6)

start_pos = Vector2(200, 400)


def start():
    print("GAME NOT WORKING YET")
    print(board)
    piece.pos = Vector2(5, 20) # use indices


def update():
    for i in range(20):
        for j in range(10):
            if board[i][j]:
                #print("draw", i, j)
                draw_square(Vector2(j * SIZE, 800-i * SIZE - SIZE), SIZE, Colors.black)

    piece.draw()

    if Input.get_key_down(K_SPACE):
        piece.rotate()
    if Input.get_key_down(K_ESCAPE):
        game.quit()
    # print("update")


game.run()
