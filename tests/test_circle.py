#!/usr/bin/env python

import unittest
import numpy as np
import sys
#sys.path.append('..')
sys.path.append('.')
import point
from circle import Circle


class CircleTester(unittest.TestCase):
    def setUp(self):
        self.c0 = Circle(point.Point(2, 3), 3)
        self.c1 = Circle(point.Point(1, -1), 4)

    def test_intersection(self):
        intersection = self.c0.intersection_with(self.c1)
        p1 = point.Point(-0.95616670564347, 2.4890416764109)
        p0 = point.Point(4.3679314115258, 1.1580171471185)
        expected = [p0, p1]
        self.assertAlmostEqual(intersection[0].x, expected[0].x)
        self.assertAlmostEqual(intersection[0].y, expected[0].y)

if __name__ == '__main__':
    unittest.main()
