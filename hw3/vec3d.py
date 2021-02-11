import copy
import math


class Vec3d:

    def __init__(self, x, y, z, w):
        self.vector = [x, y, z, w]

    @property
    def x(self):
        return self.vector[0]

    @property
    def y(self):
        return self.vector[1]

    @property
    def z(self):
        return self.vector[2]

    @property
    def w(self):
        return self.vector[3]

    @property
    def vec3d(self):
        return self.vector

    def __str__(self):
        return "Vec3d: \n\t" + self.vector.__str__()

    def copy(self):
        return copy.deepcopy(self)

    def isVector(self):
        return self.w == 0

    def isPoint(self):
        return self.w == 1

    def __add__(self, other):
        if self.w == 0.0:
            return Vec3d(self.x + other.x, self.y + other.y, self.z + other.z, 0.0)
        elif self.w == 1.0:
            return Vec3d(self.x + other.x, self.y + other.y, self.z + other.z, 1.0)

    def __sub__(self, other):
        return self.copy() + (other * -1)

    def __mul__(self, multiplier):
        return Vec3d(self.x * multiplier, self.y * multiplier, self.z * multiplier, 0.0)

    def dot_product(self, other):
        if self.vector[3] == 0:
            result = 0
            vect = other.vec3d
            for i in range(3):
                result += self.vector[i] * vect[i]
            return result

    def length(self):
        return math.sqrt(self.length_square())

    def length_square(self):
        sum = 0
        for i in range(3):
            sum += self.vector[i] ** 2
        return sum

    def angle_between_vectors(self, other):
        if self.vector[3] == 0:
            cos_theta = (self.dot_product(other)) / (self.length() * other.length())
            theta = (math.acos(cos_theta) * 180.0) / math.pi
            return theta

    def cross_product(self, other):
        a = self.vector
        b = other.vec3d
        return Vec3d((a[1] * b[2]) - (a[2] * b[1]), (a[2] * b[0]) - (a[0] * b[2]), (a[0] * b[1]) - (a[1] * b[0]), 0)

    def projection_onto(self, other):
        if self.vector[3] == 0:
            scalar = self.dot_product(other) / (float(other.dot_product(other)))
            proj = other.copy()
            proj.scalar_multiplication(scalar)
            return proj

    def normalize(self):
        if self.length() == 0:
            self *= 0
        else:
            self *= (1 / self.length())
        return self
