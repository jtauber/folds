#!/usr/bin/env python


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


# We want a test for collinearity. To do that, we'll first introduce the notion
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


def collinear(*vertices):
    d = direction(vector(vertices[0], vertices[1]))
    for vertex in vertices[2:]:
        if direction(vector(vertices[0], vertex)) != d:
            return False
    return True


v3 = Vertex(0, 2, 0)
v4 = Vertex(1, 0, 0)

assert collinear(v1, v2, v3) == True
assert collinear(v1, v2, v4) == False


# Before moving on to coplanarity, I'm going to take a moment to try
# reimplementing the collinearity test using Cayley-Menger determinants

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
    
    cayley_menger_det = (
        AB * AB + AC * AC + BC * BC
        - 2 * AB * AC - 2 * AB * BC - 2 * AC * BC
    )
    
    return cayley_menger_det == 0


assert straight(v1, v2, v3) == True
assert straight(v1, v2, v4) == False


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
    
    cayley_menger_det = (
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
    return cayley_menger_det == 0


assert plane(v1, v2, v3, v4) == True


# We can now rewrite straight as:

def better_straight(A, B, C):
    AB = square_distance(A, B)
    AC = square_distance(A, C)
    BC = square_distance(B, C)
    
    cayley_menger_det = (
        AB * AB + AC * AC + BC * BC
        - 2 * AB * AC - 2 * AB * BC - 2 * AC * BC
    )
    
    return cayley_menger_det == 0


# to model folding, we're going to want to know the foot of an altitude from
# a Vertex to an Edge.

def foot_of_altitude(vertex, edge):
    x1, y1, z1 = edge.vertex_1.coordinates
    x2, y2, z2 = edge.vertex_2.coordinates
    x3, y3, z3 = vertex.coordinates
    
    t = 1. * (
        (x1 - x2) * (x1 - x3) + (y1 - y2) * (y1 - y3) + (z1 - z2) * (z1 - z3)
    ) / ((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
    
    return Vertex(x1 + (x2 - x1) * t, y1 + (y2 - y1) * t, z1 + (z2 - z1) * t)


assert foot_of_altitude(
    Vertex(1, 2, 0), Edge(Vertex(0, 0, 0,), Vertex(2, 0, 0))
).coordinates == (1, 0, 0)


# to keep things rational, going to rewrite that using fractions.Fraction

from fractions import Fraction


def rational_foot_of_altitude(vertex, edge):
    x1, y1, z1 = edge.vertex_1.coordinates
    x2, y2, z2 = edge.vertex_2.coordinates
    x3, y3, z3 = vertex.coordinates
    
    t = Fraction(
        (x1 - x2) * (x1 - x3) + (y1 - y2) * (y1 - y3) + (z1 - z2) * (z1 - z3),
        (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2
    )
    
    return Vertex(x1 + (x2 - x1) * t, y1 + (y2 - y1) * t, z1 + (z2 - z1) * t)


assert rational_foot_of_altitude(
    Vertex(1, 2, 0), Edge(Vertex(0, 0, 0,), Vertex(2, 0, 0))
).coordinates == (1, 0, 0)


# if we have a point C and the line AB and we calculate the foot of the
# altitude from C to AB to be D, then what we now want to do is define a circle
# axis AB, centre D, radius |CD|

class Circle:
    def __init__(self, center, radius, axis):
        self.center = center
        self.radius = radius
        self.axis = axis
    
    def parameterization(self, m):
        # the rational parametrization of a unit circle at the origin in 2D is:
        # [(1-m^2)/(1+m^2), 2m/(1+m^2)]
        local_x = self.radius * Fraction(1 - m ** 2, 1 + m ** 2)
        local_y = self.radius * Fraction(2 * m, 1 + m ** 2)
        
        u_x, u_y, u_z = 1, 0, 0  # @@@
        v_x, v_y, v_z = 0, 1, 0  # @@@
        c_x, c_y, c_z = self.center.coordinates
        
        # now we need to transform that with c + xru + yrv
        global_x = c_x + local_x * u_x + local_y * v_x
        global_y = c_y + local_x * u_y + local_y * v_y
        global_z = c_z + local_x * u_z + local_y * v_z
        
        return Vertex(global_x, global_y, global_z)
