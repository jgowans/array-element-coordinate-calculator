import unittest
import numpy as np
import sys
sys.path.append('.')
import array_trilateration
from point import Point

# Sample being tested:
# 0 @ (0, 0)
# 1 @ (4, 0)
# 2 @ (3, 4)
# 3 @ (1, 5)

class ArrayTrilateration(unittest.TestCase):
    def test_four_element(self):
        p0 = Point(0, 0)
        p1 = Point(4, 0)
        p2 = Point(3, 4)
        p3 = Point(1, 5)
        d01 = p0.distance_to_other(p1)
        d02 = p0.distance_to_other(p2)
        d03 = p0.distance_to_other(p3)
        d12 = p1.distance_to_other(p2)
        d13 = p1.distance_to_other(p3)
        d23 = p2.distance_to_other(p3)
        print("0->1: {d}".format(d = d01))
        print("0->2: {d}".format(d = d02))
        print("0->3: {d}".format(d = d03))
        print("1->2: {d}".format(d = d12))
        print("1->3: {d}".format(d = d13))
        print("2->3: {d}".format(d = d23))
        array = np.array([
            [  0, d01, d02, d03], 
            [d01,   0, d12, d13],
            [d02, d12,   0, d23],
            [d03, d13, d23,   0]
        ])

        result = array_trilateration.run(4, d01, d02, d03, d12, d13, d23)
        self.assertEqual(len(result), 4)
        self.assertIn(p0, result)
        self.assertIn(p1, result)
        self.assertIn(p2, result)
        self.assertIn(p3, result)
