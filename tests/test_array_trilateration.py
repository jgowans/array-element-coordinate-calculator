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
# Baseline lengths
# 0->1: 4.0
# 0->2: 5.0
# 0->3: 5.09901951359
# 1->2: 4.12310562562
# 1->3: 5.83095189485
# 2->3: 2.2360679775

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
        self.distances = {'d01':self.d01, 
                     'd02':self.d02, 
                     'd03':self.d03, 
                     'd12':self.d12, 
                     'd13':self.d13, 
                     'd23':self.d23}

    def test_build_array(self):
        expected = np.array([
            [       0, self.d01, self.d02, self.d03], 
            [self.d01,        0, self.d12, self.d13],
            [self.d02, self.d12,        0, self.d23],
            [self.d03, self.d13, self.d23,        0]
        ])
        output = array_trilateration.build_distance_matrix_from_distances(4, self.distances)
        self.assertEqual(output.shape, expected.shape)
        self.assertTrue((output == expected).all())

    def test_four_element_noise_free(self):
        result = array_trilateration.run(4, **self.distances)
        self.assertEqual(len(result), 4)
        self.assertIn(self.p0, result)
        self.assertIn(self.p1, result)
        self.assertIn(self.p2, result)
        self.assertIn(self.p3, result)
