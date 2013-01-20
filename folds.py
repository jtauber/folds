

# We'll start with the notion of a vertex

# Because we're moving vertices around, their coordinates are inherently
# mutable # but we need references to them to build up larger structures so
# we're going to use a class containing a 3-tuple for the current coordinates

class Vertex:
    def __init__(self, x, y, z):
        self.coordinates = (x, y, z)

v1 = Vertex(0, 0, 0)
v2 = Vertex(0, 1, 0)
