import math


class Vec3d:

    def __init__(self, x, y, z, w):
        self.vector = [x, y, z, w]

    def get_x(self):
        return self.vector[0]

    def get_y(self):
        return self.vector[1]

    def get_z(self):
        return self.vector[2]

    def get_vec3d(self):
        return self.vector

    def __str__(self):
        return "Vec3d: \n\t" + self.vector.__str__()

    def copy(self):
        """ Creates a copy of vector. """
        return Vec3d(self.get_x(), self.get_y(), self.get_z(), 0)

    def add_vec3d(self, other):
        """ Performs addition between vectors.

        Args:
            other (Vec3d): Vec3d object
        """
        vect = other.get_vec3d
        for i in range(4):
            self.vector[i] += vect[i]
        return self

    def sub_vec3d(self, other):
        """ Performs substraction between vectors.

        Args:
            other (Vec3d): Vec3d object
        """
        vect = other.get_vec3d
        for i in range(4):
            self.vector[i] -= vect[i]
        return self

    def scalar_multiplication(self, multiplier):
        """ Performs scalar multiplication.

        Args:
            multiplier (float): Multiplier for multiplication
        """
        for i in range(4):
            self.vector[i] *= multiplier

    def dot_product(self, other):
        """ Finds dot product of two vectors.

        Args:
            other (Vec3d): Vec3d object

        Returns:
            result (float): Result of dot product
        """
        if self.vector[3] == 0:
            result = 0
            vect = other.get_vec3d()
            for i in range(3):
                result += self.vector[i] * vect[i]
            return result

    def length(self):
        """ Calculates length of vector. """
        return math.sqrt(self.dot_product(self))

    def angle_between_vectors(self, other):
        """ Finds angle between vectors.

        Args:
            other (Vec3d): Vec3d object

        Returns:
            theta (int): Angle between vectors
        """
        if self.vector[3] == 0:
            cos_theta = (self.dot_product(other)) / (self.length() * other.length())
            theta = (math.acos(cos_theta) * 180.0) / math.pi
            return theta

    def cross_product(self, other):
        """ Performs cross product of vectors.

        Args:
            other (Vec3d): Vec3d object

        Returns:
            Vec3d object
        """
        a = self.vector
        b = other.get_vec3d()
        return Vec3d((a[1] * b[2]) - (a[2] * b[1]), (a[2] * b[0]) - (a[0] * b[2]), (a[0] * b[1]) - (a[1] * b[0]), 0)

    def projection_onto(self, other):
        """ Finds projection of of a vector onto vector.

        Args:
            other (Vec3d): Vec3d object

        Returns:
            proj (Vec3d): Projection vector
        """
        if self.vector[3] == 0:
            scalar = self.dot_product(other) / (float(other.dot_product(other)))
            proj = other.copy()
            proj.scalar_multiplication(scalar)
            return proj
