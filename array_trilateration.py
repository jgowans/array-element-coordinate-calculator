#!/usr/bin/env python

import numpy as np
import argparse

class Point:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __eq__(self, other):
        if self.x != other.x:
            return False
        if self.y != other.y:
            return False
        return True

    def __add__(self, other):
        return Point(self.x + other.x, 
                     self.y + other.y)

    def __mul__(self, scale):
        return Point(self.x * scale,
                     self.y * scale)

    def delta_to_other(self, other):
        """ Returns a hash like {'x': delta-x, 'y': delta-y}
        """
        delta_x = other.x - self.x
        delta_y = other.y - self.y
        return Point(delta_x, delta_y)

    def distance_to_other(self, other):
        delta = self.delta_to_other(other)
        return np.sqrt(np.square(delta.x) + np.square(delta.y))

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

class Circle:
    def __init__(self, centre, r):
        self.centre = centre
        self.r = float(r)

    def distance_between_centres(self, other):
        return self.centre.distance_to_other(other.centre)

    def intersection_with(self, other):
        """ algorithm from: http://paulbourke.net/geometry/circlesphere/
        """
        d = self.distance_between_centres(other)
        if(d > (self.r + other.r)):
            raise Exception("No solution - circles are separate")
        if(d < np.abs(self.r - other.r)):
            raise Exception("No solution - once contain in the other")
        grad = self.centre.delta_to_other(other.centre)
        a = (np.square(self.r) - np.square(other.r) + np.square(d))/(2.0*d)
        p2 = self.centre + (grad * (a/d))
        h = np.sqrt(np.square(self.r) - np.square(a))
        p3 = p2 + (grad.rotated(+np.pi/2).to_unit() * h)
        p4 = p2 + (grad.rotated(-np.pi/2).to_unit() * h)
        return [p3, p4]

parser = argparse.ArgumentParser(description = "Calculate coordinates from side lengths")
