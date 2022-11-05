from dojogame.physics.rigidbody import AngularInertia
from dojogame.maths.vectors import Vector2
import unittest


class TestInertia(unittest.TestCase):
    def test_static_inertia(self):
        self.assertEqual(AngularInertia.calculate_moment_of_inertia([Vector2(.5, .5),
                                                                      Vector2(-.5, .5),
                                                                      Vector2(-.5, -.5),
                                                                      Vector2(.5, -.5)],
                                                                     1),
                         AngularInertia.calculate_moment_of_inertia(
                             [Vector2(0, 0), Vector2(1, 0), Vector2(1, 1), Vector2(0, 1)], 1))
