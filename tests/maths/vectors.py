from dojogame.maths.vectors import Vector2
import unittest


class VectorTest(unittest.TestCase):
    def test_add(self):
        a = Vector2(1, 2)
        b = Vector2(3, 4)
        self.assertEqual(a + b, Vector2(4, 6))

    def test_sub(self):
        a = Vector2(1, 2)
        b = Vector2(3, 4)
        self.assertEqual(a - b, Vector2(-2, -2))

    def test_neg(self):
        a = Vector2(1, 2)
        self.assertEqual(-a, Vector2(-1, -2))

    def test_mul(self):
        a = Vector2(1, 2)
        self.assertEqual(a * 2, Vector2(2, 4))
        self.assertEqual(2 * a, Vector2(2, 4))

    def test_div(self):
        a = Vector2(1, 2)
        self.assertEqual(a / 2, Vector2(0.5, 1))

    def test_cross(self):
        a = Vector2(1, 2)
        b = Vector2(3, 4)
        self.assertEqual(Vector2.cross(a, b), -2)
        c = Vector2(1, 0)
        d = Vector2(0, 1)
        self.assertEqual(Vector2.cross(c, d), 1)

    def test_dot(self):
        a = Vector2(1, 2)
        b = Vector2(3, 4)
        self.assertEqual(Vector2.dot(a, b), 11)
