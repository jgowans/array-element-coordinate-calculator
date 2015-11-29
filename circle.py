import numpy as np

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
            print(self.centre)
            print(self.r)
            print(other.centre)
            print(other.r)
            raise Exception("No solution - circles are separate")
        if(d < np.abs(self.r - other.r)):
            print(self.centre)
            print(self.r)
            print(other.centre)
            print(other.r)
            raise Exception("No solution - once contain in the other")
        grad = self.centre.delta_to_other(other.centre)
        a = (np.square(self.r) - np.square(other.r) + np.square(d))/(2.0*d)
        p2 = self.centre + (grad * (a/d))
        h = np.sqrt(np.square(self.r) - np.square(a))
        p3 = p2 + (grad.rotated(+np.pi/2).to_unit() * h)
        p4 = p2 + (grad.rotated(-np.pi/2).to_unit() * h)
        return [p3, p4]

    def positive_intersection_with(self, other):
        points = self.intersection_with(other)
        positive_y = [point for point in points if point.y > 0]
        assert(len(positive_y) == 1)
        return positive_y[0]
