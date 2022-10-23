from dojogame.dojographics.gameobjects import GameObject
from dojogame.dojomaths.transform import Transform
from dojogame.dojomaths.vectors import Vector2


class Button(GameObject):
    def __init__(self, background: GameObject, foreground: GameObject = None):
        super().__init__()
        self.transform = Transform(game_object=self)
        self.background = background
        self.foreground = foreground

        self.background.transform.set_parent(self.transform)
        self.background.transform.set_position(Vector2.zero())
        self.background.transform.local_position = Vector2.zero()

        if self.foreground is not None:
            self.foreground.transform.set_parent(self.background.transform)
            self.foreground.transform.set_position(Vector2.zero())

    def draw(self, screen):
        self.background.draw(screen)
        if self.foreground is not None:
            self.foreground.draw(screen)
