import math
import numpy as np


# distance between 2 points
def p2p_dist(p1, p2):
    dy = (p2[1] - p1[1])
    dx = (p2[0] - p1[0])
    return math.sqrt(dy * dy + dx * dx)


# weighted average of two points
def p_avgw(p1,p2,w):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return p1[0] + dx * (1-w), p1[1] + dy * (1-w)


# average of two points
def p_avg(p1, p2):
    return (p1[0] + p2[0]) * 0.5, (p1[1] + p2[1]) * 0.5


# weighted average of two lines
def l_avgw(l1,l2,w):
    p1 = p_avgw(l1.points[0], l2.points[0], w)
    p2 = p_avgw(l1.points[1], l2.points[1], w)
    return Line(p1, p2)

# average of two lines
def l_avg(l1, l2):
    p1 = p_avg(l1.points[0], l2.points[0])
    p2 = p_avg(l1.points[1], l2.points[1])
    return Line(p1, p2)


# class defining a line
class Line:
    # create a line from 2 points
    def __init__(self, point1, point2):
        self.slope = (point2[1] - point1[1]) / (point2[0] - point1[0] + 0.1)
        self.points = [point1, point2]

    # returns the distance from the line to a point
    def l2p_dist(self, p):
        p1 = self.points[0]
        p2 = self.points[1]
        return ((p1[1] - p2[1]) * p[0] - (p1[0] - p2[0]) * p[1] + p1[0] * p2[1] - p1[1] * p2[0]) / p2p_dist(p1, p2)


# class defining a quadrilateral
class Quad:
    # create a quadrilateral from a list of points in arbitrary order
    def __init__(self, points):
        points = sorted(points, key=lambda p: p[0])

        left = points[:2]
        right = points[2:]
        left = sorted(left, key=lambda p: p[1])
        right = sorted(right, key=lambda p: p[1])
        self.points = [left[0], right[0], left[1], right[1]]  # tl, tr, bl, br
        l_top = Line(left[0], right[0])
        l_right = Line(right[1], right[0])
        l_bottom = Line(left[1], right[1])
        l_left = Line(left[1], left[0])
        # self.lines = [l_top, l_bottom, l_left, l_right]
        self.lines = [l_avgw(l_top, l_bottom, 0.85), l_avgw(l_bottom, l_top, 0.95), l_avgw(l_left, l_right, 0.95), l_avgw(l_right, l_left, 0.95)]  # top, bottom, left, right

    def get_points(self):
        return np.array([self.points[0], self.points[1], self.points[3], self.points[2]])

    # returns true if p is in the quadrilateral
    def contains(self, p):
        return self.lines[0].l2p_dist(p) > 0 and self.lines[1].l2p_dist(p) < 0 and \
               self.lines[2].l2p_dist(p) < 0 and self.lines[3].l2p_dist(p) > 0

    # recursive function to detect what fraction between lines l1 and l2 the point p is
    def frac(self, p, l1, l2, min_f, max_f):
        # if out of range, return -1
        if l1.l2p_dist(p) < 0:
            return 0
        if l2.l2p_dist(p) > 0:
            return 1
        # if close enough, return fraction
        l3 = l_avg(l1, l2)
        g = l3.l2p_dist(p)
        if abs(g) < 0.01:
            return (max_f + min_f) / 2
        # otherwise, binary search
        half = (max_f - min_f) / 2
        if g > 0:
            return self.frac(p, l3, l2, min_f + half, max_f)
        else:
            return self.frac(p, l1, l3, min_f, max_f - half)

    # returns the the point p in fractional screen coordinates
    def convert(self, p):
        f_y = self.frac(p, self.lines[0], self.lines[1], 0.0, 1.0)
        f_x = self.frac(p, self.lines[2], self.lines[3], 0.0, 1.0)
        return f_x, 1-f_y


#
# a1 = (0, 0)
# a2 = (0, 100)
# a3 = (100, 0)
# a4 = (100, 100)
# a5 = (50, 50)
# q = Quad([a1, a2, a3, a4])
# # for point in q.points:
# #     print point
# # print q.convert(a5)
# print q.lines[1].points