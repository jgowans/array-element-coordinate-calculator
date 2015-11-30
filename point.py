import numpy as np
import argparse

class Point:
    """ Sort of a point, sort of a vector.
    There's not too much difference, is there??... 
    """
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __eq__(self, other):
        if round(self.x, 7) != round(other.x, 7):
            return False
        if round(self.y, 7) != round(other.y, 7):
            return False
        return True

    def __add__(self, other):
        return Point(self.x + other.x, 
                     self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, 
                     self.y - other.y)

    def __mul__(self, scale):
        return Point(self.x * scale,
                     self.y * scale)

    def __div__(self, scale):
        return Point(self.x/float(scale), self.y/float(scale))

    def __repr__(self):
        return "({x}, {y})".format(x = self.x, y = self.y)

    def delta_to_other(self, other):
        """ Returns a hash like {'x': delta-x, 'y': delta-y}
        """
        delta_x = other.x - self.x
        delta_y = other.y - self.y
        return Point(delta_x, delta_y)

    def distance_to_other(self, other):
        delta = self.delta_to_other(other)
        return np.sqrt(np.square(delta.x) + np.square(delta.y))

    def get_closest(self, others):
        """ Others is a list of points. 
        Return the point in others which is closest to thi
        """
        smallest_distance = self.distance_to_other(others[0])
        best_point = others[0]
        for other in others:
            distance = self.distance_to_other(other)
            if distance < smallest_distance:
                smallest_distance = distance
                best_point = other
        return best_point

    def rotated(self, phi):
        """ Counterclockwise rotation by phi  radians
        """
        rotation_matrix = np.array([
                [np.cos(phi), -np.sin(phi)],
                [np.sin(phi), np.cos(phi)]
        ])
        new_location = rotation_matrix.dot(np.array([ [self.x], [self.y] ]))
        return Point(new_location[0,0], new_location[1,0])

    def to_unit(self):
        l = np.sqrt(np.square(self.x) + np.square(self.y))
        return Point(self.x/l, self.y/l)
