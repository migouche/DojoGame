from dojogame.maths.vectors import Vector2
from dojogame.data.enums import Space, ForceMode
from dojogame.maths.realtime import RealTime
from dojogame.graphics.gameobjects import GameObject


#  requires A LOT of rework

class Action:
    def __init__(self, dSpeed: Vector2 = Vector2.zero(), dAngle: float = 0):
        self.dSpeed = dSpeed
        self.dAngle = dAngle

    def __add__(self, other) -> 'Action':
        return Action(self.dSpeed + other.dSpeed, self.dAngle + other.dAngle)


class Rigidbody:
    def __init__(self, game_object: GameObject, mass: float = 1):
        self.game_object = game_object
        self.totalAction = Action()
        self.velocity = Vector2.zero()
        self.angularVelocity = 0
        self.mass = mass
        self.kinematic = False
        self.useGravity = False  # May use it later, may not

    def add_force_at_position(self, force: Vector2, position: Vector2,
                              mode: ForceMode = ForceMode.Force,
                              space: Space = Space.World):

        if space == Space.Self:
            absolute_pos = self.game_object.transform.relative_pos_to_absolute(position)
            absolute_force = Vector2.rotate_by_degs(force, self.game_object.transform.rotation)

            self.add_force_at_position(absolute_force, absolute_pos, mode, Space.World)
            return
        pos_rel = position - self.game_object.transform.position if space == Space.World else None
        if pos_rel is None:
            raise TypeError("Wrong Space given")

        if mode == ForceMode.Force:  # dv = F * dt / m
            self.totalAction += Action(f := force * RealTime.delta_time / self.mass, Vector2.cross(pos_rel, f))
        elif mode == ForceMode.Acceleration:  # dv = F * dt
            self.totalAction += Action(f := force * RealTime.delta_time, Vector2.cross(pos_rel, f))
        elif mode == ForceMode.Impulse:  # dv = F / m
            self.totalAction += Action(f := force / self.mass, Vector2.cross(pos_rel, f))
        elif mode == ForceMode.VelocityChange:  # dv = F
            self.totalAction += Action(f := force, Vector2.cross(pos_rel, f))
        else:
            raise TypeError("Wrong ForceMode given")

    def add_force(self, force: Vector2, mode: ForceMode = ForceMode.Force):
        self.add_force_at_position(force, self.game_object.transform.position, mode)

    def update_action(self):
        self.velocity += self.totalAction.dSpeed
        self.angularVelocity += self.totalAction.dAngle

        self.game_object.transform.position += self.velocity * RealTime.delta_time
        self.game_object.transform.rotation += self.angularVelocity * RealTime.delta_time

        self.totalAction = Action()

    @staticmethod
    def add_rigidbody(game_object, mass: float = 1) -> GameObject:
        game_object._rigidbody = Rigidbody(game_object, mass)
        return game_object
