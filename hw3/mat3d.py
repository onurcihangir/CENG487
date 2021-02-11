import math
from vec3d import Vec3d


class Mat3d:

    def __init__(self):
        self.matrix = [[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]]

    def vecmul(self, a_vec3d):
        """ Multiplies matrix with vector.

        Args:
            a_vec3d (Vec3d): Vec3d object

        Returns:
            Vec3d object
        """
        vect = a_vec3d.vec3d
        result = [0, 0, 0, 0]
        for i in range(4):
            for j in range(4):
                result[i] += self.matrix[i][j] * vect[j]
        return Vec3d(result[0], result[1], result[2], result[3])

    def matmul(self, a_mat3d):
        """ Multiplies matrix with matrix.

        Args:
            a_mat3d (Mat3d): Mat3d object

        """
        matr = [[0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]]
        for i in range(4):
            for j in range(4):
                sum = 0
                for k in range(4):
                    sum += self.matrix[i][k] * a_mat3d.matrix[k][j]
                matr[i][j] = sum
        self.matrix = matr
        return self

    def transpose(self):
        """ Transposes the matrix. """
        matr = [[0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]]
        for i in range(4):
            for j in range(4):
                matr[i][j] = self.matrix[j][i]
        self.matrix = matr
        return self

    def define_scaling_matrix(self, sx, sy, sz):
        """ Defines a scaling matrix.

        Args:
            sx (float): multiplier for x
            sy (float): multiplier for y
            sz (float): multiplier for z

        """
        self.__init__()
        scale_list = [sx, sy, sz, 1]
        for i in range(4):
            self.matrix[i][i] = scale_list[i]
        return self

    def define_translation_matrix(self, dx, dy, dz):
        """ Defines a translation matrix.

            Args:
                dx (float): multiplier for x
                dy (float): multiplier for y
                dz (float): multiplier for z

        """
        self.__init__()
        t_list = [dx, dy, dz, 1]
        for i in range(4):
            self.matrix[i][3] = t_list[i]
        return self

    def define_rotation_matrix(self, theta, axis):
        """ Defines a rotation matrix.

            Args:
                theta (int): angle for rotation
                axis (String): axis name for rotation

        """
        self.__init__()
        radian = theta * (math.pi / 180)
        cosx = math.cos(radian)
        sinx = math.sin(radian)
        if axis == "x":
            self.matrix[1][1] = cosx
            self.matrix[2][1] = sinx
            self.matrix[1][2] = -sinx
            self.matrix[2][2] = cosx
        elif axis == "y":
            self.matrix[0][0] = cosx
            self.matrix[2][0] = -sinx
            self.matrix[0][2] = sinx
            self.matrix[2][2] = cosx
        elif axis == "z":
            self.matrix[0][0] = cosx
            self.matrix[1][0] = sinx
            self.matrix[0][1] = -sinx
            self.matrix[1][1] = cosx
        else:
            return "Enter valid axis!! (e.g. 'x')"
        return self

    def __str__(self):
        output = "Mat3d: \n\t"
        for i in self.matrix:
            output += str(i) + "\n\t"
        return output
