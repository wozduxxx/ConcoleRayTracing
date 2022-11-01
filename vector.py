from math import sqrt, sin, cos


class Vector3:
    '''Realization of 3D Vector and operations on it'''

    def __init__(self, x=.0, y=.0, z=.0):
        self.x = x
        self.y = y
        self.z = z
        self.components = [self.x, self.y, self.z]

    def __iter__(self):
        return iter(self.components)

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)

    def __truediv__(self, other):
        if type(other) == int or type(other) == float:
            other = Vector3(other, other, other)
        if other.z != 0:
            return Vector3(self.x / other.x, self.y / other.y, self.z / other.z)
        else:
            return Vector3(self.x / other.x, self.y / other.y, 0)

    def __abs__(self) -> float:
        return sqrt(sum(x*x for x in self))

    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)

    def __repr__(self) -> str:
        return f'Vector3(x={self.x}, y={self.y}, z={self.z})'

    def norm(self):
        '''Normalization of the vector'''
        try:
            return self / abs(self)
        except ZeroDivisionError:
            return Vector3()

    def sign(self):
        return Vector3(sign(self.x), sign(self.y), sign(self.z))

    def step(self, edge):
        return Vector3(step(edge.x, self.x), step(edge.y, self.y), step(edge.z, self.z),)


    def rotate_x(self, angle: float):
        vec = Vector3(self.x, self.y, self.z)
        vec.z = self.z * cos(angle) - self.y * sin(angle)
        vec.y = self.z * sin(angle) + self.y * cos(angle)
        return vec

    def rotate_y(self, angle: float):
        vec = Vector3(self.x, self.y, self.z)
        vec.x = self.x * cos(angle) - self.z * sin(angle)
        vec.z = self.x * sin(angle) + self.z * cos(angle)
        return vec

    def rotate_z(self, angle: float):
        vec = Vector3(self.x, self.y, self.z)
        vec.x = self.x * cos(angle) - self.y * sin(angle)
        vec.y = self.x * sin(angle) + self.y * cos(angle)
        return vec


def dot(vec1: Vector3, vec2: Vector3) -> float:
    '''Dot multiply'''
    return vec1.x * vec2.x + vec1.y * vec2.y + vec1.z * vec2.z


def border(value, minv, maxv) -> float:
    '''Calculate restrictions of value'''
    return max(min(value, maxv), minv)


def sign(n):
    return int((n > 0) - (n < 0))


def step(edge, n):
    return int(n > edge)


def vector_step(edge, v):
    '''Calculate step for vectors only'''
    return Vector3(step(edge.x, v.x), step(edge.y, v.y), step(edge.z, v.z))


def smoothstep(edge0: float, edge1: float, x: float) -> float:
    x = border((x - edge0) / (edge1 - edge0), 0, 1)
    return x * x * (3 - 2 * x)

def reflect(rd: Vector3, n: Vector3):
    '''Calculate reflections'''
    return rd - n * (Vector3(2, 2, 2) * Vector3(dot(n, rd), dot(n, rd), dot(n, rd)))
