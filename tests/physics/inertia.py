from dojogame.physics.rigidbody import AngularInertia
from dojogame.maths.vectors import Vector2
import unittest


class TestInertia(unittest.TestCase):
    def test_densities(self):
        # Square
        square = AngularInertia.Polygon([Vector2(0, 0), Vector2(1, 0), Vector2(1, 1), Vector2(0, 1)], 1)
        self.assertEqual(square.density, 1)


    def test_static_inertia(self):
        self.assertEqual(AngularInertia.calculate_moment_of_inertia2([Vector2(1+.5, .5),
                                                                      Vector2(1+-.5, .5),
                                                                      Vector2(1+-.5, -.5),
                                                                      Vector2(1+.5, -.5)],
                                                                     1), 2 * (1 / 4 + 1 / 12))
