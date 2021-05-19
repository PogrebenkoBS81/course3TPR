import numpy as np


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, dot1, dot2, legend):
        self.dot1 = dot1
        self.dot2 = dot2
        self.legend = legend

    def line_intersection(self, other):
        a1 = (self.dot1.x, self.dot1.y)
        a2 = (self.dot2.x, self.dot2.y)

        b1 = (other.dot1.x, other.dot1.y)
        b2 = (other.dot2.x, other.dot2.y)

        s = np.vstack([a1, a2, b1, b2])  # s for stacked
        h = np.hstack((s, np.ones((4, 1))))  # h for homogeneous
        l1 = np.cross(h[0], h[1])  # get first line
        l2 = np.cross(h[2], h[3])  # get second line
        x, y, z = np.cross(l1, l2)  # point of intersection

        if z == 0:  # lines are parallel
            return float('inf'), float('inf')

        return x / z, y / z
