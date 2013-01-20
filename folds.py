

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


# We want a test for colinearity. To do that, we'll first introduce the notion
# of a 3-tuple "vector", the conversion to spherical coordinates to get a
# "direction" and then finally a test for whether two vectors are
# parallel or not

def vector(vertex_1, vertex_2):
    return tuple(c1 - c2 for c1, c2 in
        zip(vertex_1.coordinates, vertex_2.coordinates))

# (we could rewrite "distance" above to use this)

from math import acos, atan2


def direction(vector):
    r = sqrt(sum(c ** 2 for c in vector))
    theta = acos(vector[2] / r)
    phi = atan2(vector[1], vector[0])
    return (theta, phi)


assert vector(v1, v2) == (0, -1, 0)
assert direction(vector(v1, v2)) == (1.5707963267948966, -1.5707963267948966)


def colinear(*vertices):
    d = direction(vector(vertices[0], vertices[1]))
    for vertex in vertices[2:]:
        if direction(vector(vertices[0], vertex)) != d:
            return False
    return True


v3 = Vertex(0, 2, 0)
v4 = Vertex(1, 0, 0)

assert colinear(v1, v2, v3) == True
assert colinear(v1, v2, v4) == False


# Before moving on to coplanarity, I'm going to take a moment to try
# reimplementing the colinearity test using Cayley-Menger determinants

# simplifying the 4x4 Cayley-Menger determinant for determining whether three
# elements are "straight", we get:
#
# det = AB^2 - 2 AB AC + AC^2 - 2 AB BC - 2 AC BC + BC^2
#
# where AB, AC and BC are the square of the distance

def straight(A, B, C):
    AB = distance(A, B) ** 2
    AC = distance(A, C) ** 2
    BC = distance(B, C) ** 2
    
    cayley_mengler_det = (
        AB * AB + AC * AC + BC * BC
        - 2 * AB * AC - 2 * AB * BC - 2 * AC * BC
    )
    
    return cayley_mengler_det == 0


assert(straight(v1, v2, v3)) == True
assert(straight(v1, v2, v4)) == False


# The simplification of the 5x5 is:
#
# det = -2 AB AC BC + 2 AB AD BC + 2 AC AD BC - 2 AD^2 BC - 2 AD BC^2 +
# 2 AB AC BD - 2 AC^2 BD - 2 AB AD BD + 2 AC AD BD + 2 AC BC BD +
# 2 AD BC BD - 2 AC BD^2 - 2 AB^2 CD + 2 AB AC CD + 2 AB AD CD -
# 2 AC AD CD + 2 AB BC CD + 2 AD BC CD + 2 AB BD CD + 2 AC BD CD -
# 2 BC BD CD - 2 AB CD^2

# where AB, AC, AD, BC, BD, CD are squares of the distance

# Because taking a square root in distance() then squaring again can lead to
# imprecision which results in a determinant very close but not quite zero
# when it really should be zero, we'll use a square_distance function:


def square_distance(vertex_1, vertex_2):
    return sum((c1 - c2) ** 2 for c1, c2 in
        zip(vertex_1.coordinates, vertex_2.coordinates))


def plane(A, B, C, D):
    AB = square_distance(A, B)
    AC = square_distance(A, C)
    AD = square_distance(A, D)
    BC = square_distance(B, C)
    BD = square_distance(B, D)
    CD = square_distance(C, D)
    
    cayley_mengler_det = (
        - 2 * AB * AB * CD
        - 2 * AB * AC * BC
        + 2 * AB * AC * BD
        + 2 * AB * AC * CD
        + 2 * AB * AD * BC
        - 2 * AB * AD * BD
        + 2 * AB * AD * CD
        + 2 * AB * BC * CD
        + 2 * AB * BD * CD
        - 2 * AB * CD * CD

        - 2 * AC * AC * BD
        + 2 * AC * AD * BC
        + 2 * AC * AD * BD
        - 2 * AC * AD * CD
        + 2 * AC * BC * BD
        - 2 * AC * BD * BD
        + 2 * AC * BD * CD

        - 2 * AD * AD * BC
        - 2 * AD * BC * BC
        + 2 * AD * BC * BD
        + 2 * AD * BC * CD
        
        - 2 * BC * BD * CD
    )
    return cayley_mengler_det == 0


assert plane(v1, v2, v3, v4) == True


# We can now rewrite straight as:

def better_straight(A, B, C):
    AB = square_distance(A, B)
    AC = square_distance(A, C)
    BC = square_distance(B, C)
    
    cayley_mengler_det = (
        AB * AB + AC * AC + BC * BC
        - 2 * AB * AC - 2 * AB * BC - 2 * AC * BC
    )
    
    return cayley_mengler_det == 0
