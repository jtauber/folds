from fractions import Fraction


class Vertex:
    def __init__(self, x, y, z):
        self.coordinates = (x, y, z)
    
    def __eq__(self, other):
        return (isinstance(other, Vertex) and
            self.coordinates == other.coordinates)


def quadrance(vertex_1, vertex_2):
    return sum((c1 - c2) ** 2 for c1, c2 in
        zip(vertex_1.coordinates, vertex_2.coordinates))


def collinear(vertex_1, vertex_2, vertex_3):
    q12 = quadrance(vertex_1, vertex_2)
    q13 = quadrance(vertex_1, vertex_3)
    q23 = quadrance(vertex_2, vertex_3)
    
    cayley_menger_det = (
        q12 * q12 + q13 * q13 + q23 * q23
        - 2 * q12 * q13 - 2 * q12 * q23 - 2 * q13 * q23
    )
    
    return cayley_menger_det == 0


class Edge:
    def __init__(self, vertex_1, vertex_2):
        self.vertex_1 = vertex_1
        self.vertex_2 = vertex_2

    def __eq__(self, other):
        return (isinstance(other, Edge) and
            self.vertex_1 == other.vertex_1 and
            self.vertex_2 == other.vertex_2)
    
    def quadrance(self):
        return quadrance(self.vertex_1, self.vertex_2)


def foot_of_altitude(vertex, edge):
    x1, y1, z1 = edge.vertex_1.coordinates
    x2, y2, z2 = edge.vertex_2.coordinates
    x3, y3, z3 = vertex.coordinates
    
    t = Fraction(
        (x1 - x2) * (x1 - x3) + (y1 - y2) * (y1 - y3) + (z1 - z2) * (z1 - z3),
        (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2
    )
    
    return Vertex(x1 + (x2 - x1) * t, y1 + (y2 - y1) * t, z1 + (z2 - z1) * t)
