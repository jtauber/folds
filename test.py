#!/usr/bin/env python


from folds import *

v1 = Vertex(0, 0, 0)
v2 = Vertex(0, 1, 0)


assert quadrance(v1, v2) == 1


e1 = Edge(v1, v2)

assert e1.quadrance() == 1


v3 = Vertex(0, 2, 0)
v4 = Vertex(1, 0, 0)

assert collinear(v1, v2, v3) == True
assert collinear(v1, v2, v4) == False


v5 = Vertex(1, 2, 0)
v6 = Vertex(2, 0, 0)

e2 = Edge(v1, v6)

assert foot_of_altitude(v5, e2) == v4
