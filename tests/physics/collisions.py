from dojogame.maths.vectors import Vector2
from dojogame.physics.collisions import Collisions

import unittest


class CollisionDetection(unittest.TestCase):
    def test_segment_segment_collision(self):
        # Test 1: No collision
        self.assertTrue(
            not Collisions.segment_intersect_segment(
                Vector2(0, 0), Vector2(1, 1), Vector2(2, 2), Vector2(3, 3)))
        # Test 2: Collision
        self.assertTrue(
            Collisions.segment_intersect_segment(
                Vector2(0, 0), Vector2(1, 1), Vector2(1, 0), Vector2(0, 1)))
        # Test 3: Test Collision point
        self.assertEqual(Collisions.segment_intersect_segment(
            Vector2(0, 0), Vector2(1, 1), Vector2(1, 0),
            Vector2(0, 1)).get_contact(0).point, Vector2(0.5, 0.5))
