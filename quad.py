import math

class Line:
    def __init(self, point1, point2, vert):
        self.slope = (point2[1] - point1[1]) / (point2[0] - point1[0])
        self.points = [point1, point2]
        self.vert = vert

    def p2p_dist(self, p1, p2):
        dy = (p2[1]-p1[1])
        dx = (p2[0]-p1[0])
        return math.sqrt(dy*dy - dx*dx)

    def l2p_dist(self, p):
        p1 = self.points[1]
        p2 = self.points[2]
        return ((p1[1]-p2[1])*p[0] - (p1[0]-p2[0])*p[1] + p1[0]*p2[1] - p1[1]*p2[0])/self.p2p_dist(p1,p2)

    def offset(self, point):
        if self.vert:
            return

# class Quad:
#     def __init__(self, points):
#         self.points = points
#
#     def contains(self, points):
#         pass
#
#     def convert(self, point):

