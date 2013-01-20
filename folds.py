

# We'll start with the notion of a vertex

# Because we're moving vertices around, their coordinates are inherently
# mutable # but we need references to them to build up larger structures so
# we're going to use a class containing a 3-tuple for the current coordinates

class Vertex:
    def __init__(self, x, y, z):
        self.coordinates = (x, y, z)

v1 = Vertex(0, 0, 0)
v2 = Vertex(0, 1, 0)


# Next we define a distance function that takes two vertices

from math import sqrt


def distance(vertex_1, vertex_2):
    return sqrt(sum((c1 - c2) ** 2 for c1, c2 in
        zip(vertex_1.coordinates, vertex_2.coordinates)))


assert distance(v1, v2) == 1.0


# An Edge pairs two vertices together

class Edge:
    def __init__(self, vertex_1, vertex_2):
        self.vertex_1 = vertex_1
        self.vertex_2 = vertex_2
    
    def length(self):
        return distance(self.vertex_1, self.vertex_2)


e1 = Edge(v1, v2)

assert e1.length() == 1.0
