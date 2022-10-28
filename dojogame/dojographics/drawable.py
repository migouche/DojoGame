# drawable.py
from dojogame.dojodata.arrays import drawables


class Drawable():
    def __init__(self, persistent: bool):
        self.persistent = persistent
        drawables.append(self)

    def update(self, screen: 'pygame.Surface') -> 'pygame.Rect':
        self.draw(screen)

    def draw(self, screen: 'pygame.Surface') -> 'pygame.Rect':
        raise NotImplementedError
