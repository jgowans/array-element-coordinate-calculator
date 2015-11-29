#/usr/bin/env python

import unittest
import numpy as np
import sys
#sys.path.append('..')
sys.path.append('.')
from point import Point


class PointTester(unittest.TestCase):
    def setUp(self):
        self.p0 = Point(2, 3)
        self.p1 = Point(3, 5)

    def test_add(self):
        addition = self.p0 + self.p1
        self.assertEqual(addition.x, 5)
        self.assertEqual(addition.y, 8)

    def test_mul(self):
        mult = self.p0 * 4.4
        self.assertAlmostEqual(mult.x, 2*4.4)
        self.assertAlmostEqual(mult.y, 3*4.4)

    def test_delta(self):
        delta = self.p0.delta_to_other(self.p1)
        self.assertEqual(delta.x, 1)
        self.assertEqual(delta.y, 2)

    def test_distance(self):
        dist = self.p0.distance_to_other(self.p1)
        self.assertEqual(dist, np.sqrt(1 + 4))

    def test_rotated(self):
        rotated = self.p0.rotated(np.pi/2)
        self.assertAlmostEqual(rotated.x, -3)
        self.assertAlmostEqual(rotated.y, 2)

    def test_comparison(self):
        self.assertNotEqual(self.p0, self.p1)
        p0_dup = Point(self.p0.x, self.p0.y)
        self.assertEqual(self.p0, p0_dup)

    def test_average(self):
        points = [self.p0, self.p1, self.p1]
        expected = Point((self.p0.x + self.p1.x + self.p1.x)/3.0,
                         (self.p0.y + self.p1.y + self.p1.y)/3.0)
        actual = sum(points, Point(0,0))/len(points)  # starting element is Point(0,0)
        self.assertEqual(expected, actual)

    def test_closest(self):
        p0 = Point(0, 0)
        p1 = Point(1, 1)
        p2 = Point(2, 2)
        p3 = Point(3, 3)
        p4 = Point(4, 4)
        self.assertEqual(p2, Point(2, 2.5).get_closest([p0, p1, p2, p3, p4]))
