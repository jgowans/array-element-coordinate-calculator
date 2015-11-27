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
    def setUp(self):
        self.p0 = Point(0, 0)
        self.p1 = Point(4, 0)
        self.p2 = Point(3, 4)
        self.p3 = Point(1, 5)
        self.d01 = self.p0.distance_to_other(self.p1)
        self.d02 = self.p0.distance_to_other(self.p2)
        self.d03 = self.p0.distance_to_other(self.p3)
        self.d12 = self.p1.distance_to_other(self.p2)
        self.d13 = self.p1.distance_to_other(self.p3)
        self.d23 = self.p2.distance_to_other(self.p3)
        print("0->1: {d}".format(d = self.d01))
        print("0->2: {d}".format(d = self.d02))
        print("0->3: {d}".format(d = self.d03))
        print("1->2: {d}".format(d = self.d12))
        print("1->3: {d}".format(d = self.d13))
        print("2->3: {d}".format(d = self.d23))

    def test_build_array(self):
        expected = np.array([
            [       0, self.d01, self.d02, self.d03], 
            [self.d01,        0, self.d12, self.d13],
            [self.d02, self.d12,        0, self.d23],
            [self.d03, self.d13, self.d23,        0]
        ])
        distances = {'d01':self.d01, 
                     'd02':self.d02, 
                     'd03':self.d03, 
                     'd12':self.d12, 
                     'd13':self.d13, 
                     'd23':self.d23}
        output = array_trilateration.build_distance_matrix(4, **distances)
        self.assertEqual(output.shape, expected.shape)
        self.assertTrue((output == expected).all())

    def skip_test_four_element(self):
        array = np.array([
            [  0, d01, d02, d03], 
            [d01,   0, d12, d13],
            [d02, d12,   0, d23],
            [d03, d13, d23,   0]
        ])
        result = array_trilateration.run(4, distances)
        self.assertEqual(len(result), 4)
        self.assertIn(p0, result)
        self.assertIn(p1, result)
        self.assertIn(p2, result)
        self.assertIn(p3, result)
