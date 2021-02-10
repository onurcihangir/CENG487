from mat3d import Mat3d
from vec3d import Vec3d


class Object:

    def __init__(self):
        self.vertices = []
        self.transformation_matrix_stack = []
        self.final_transformation_matrix = Mat3d()

    def add_vertex(self, vertex):
        """ Adds vertex to the object

        Args:
            vertex (Vec3d): Vec3d object

        """
        self.vertices.append(vertex)

    def transform_object(self, a_mat3d):
        """ Perform transformation

        Args:
            a_mat3d (Mat3d): Mat3d object
        """
        for i in range(len(self.vertices)):
            self.vertices[i] = a_mat3d.multiply_by_vec3d(self.vertices[i])
        return self

    def add_transformation(self, a_mat3d):
        """ Adds transformation matrix to the matrix stack and multiply matrix with other transformations.

        Args:
            a_mat3d (Mat3d): Mat3d object

        """
        if len(self.transformation_matrix_stack) == 0:
            self.final_transformation_matrix = a_mat3d
        else:
            self.final_transformation_matrix = a_mat3d.multiply_by_mat3d(self.final_transformation_matrix)
        self.transformation_matrix_stack.append(a_mat3d)
        return self

    def get_final_transformation_matrix(self):
        """ Returns final transformation matrix.

        Returns:
            self.final_transformation_matrix (Mat3d): Mat3d object
        """
        return self.final_transformation_matrix
