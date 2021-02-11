from mat3d import Mat3d
from vec3d import Vec3d
from OpenGL.GL import *
from OpenGL.GLUT import *


class Object:

    def __init__(self):
        self.vertices = []
        self.faces = []
        self.subdivision_level = 0
        self.original_vertices = []
        self.transformation_matrix_stack = []
        self.final_transformation_matrix = Mat3d()

    def add_vertex(self, vertex):
        """ Adds vertex to the object

        Args:
            vertex (Vec3d): Vec3d object

        """
        self.vertices.append(vertex)
        self.original_vertices.append(vertex)

    def transform_object(self, a_mat3d):
        """ Perform transformation

        Args:
            a_mat3d (Mat3d): Mat3d object
        """
        for i in range(len(self.vertices)):
            self.vertices[i] = a_mat3d.vecmul(self.vertices[i])
        return self

    def add_transformation(self, a_mat3d):
        """ Adds transformation matrix to the matrix stack and multiply matrix with other transformations.

        Args:
            a_mat3d (Mat3d): Mat3d object

        """
        if len(self.transformation_matrix_stack) == 0:
            self.final_transformation_matrix = a_mat3d
        else:
            self.final_transformation_matrix = a_mat3d.matmul(self.final_transformation_matrix)
        self.transformation_matrix_stack.append(a_mat3d)
        return self

    def get_final_transformation_matrix(self):
        """ Returns final transformation matrix.

        Returns:
            self.final_transformation_matrix (Mat3d): Mat3d object
        """
        return self.final_transformation_matrix

    def add_subdivision(self):
        temp_faces = []
        center = None
        for face in self.faces:
            center = Vec3d((face[0].x + face[2].x) / 2, (face[0].y + face[2].y) / 2,
                           (face[0].z + face[2].z) / 2, 1.0)
            for i in range(len(face)):
                v2 = Vec3d(0, 0, 0, 1.0)
                v4 = Vec3d(0, 0, 0, 1.0)
                next_index = i + 1

                if i + 1 == len(face):
                    next_index = 0

                v1 = face[i]

                v2 = Vec3d((face[i].x + face[next_index].x) / 2, (face[i].y + face[next_index].y) / 2,
                           (face[i].z + face[next_index].z) / 2, 1.0)

                v3 = center

                v4 = Vec3d((face[i].x + face[i - 1].x) / 2, (face[i].y + face[i - 1].y) / 2,
                           (face[i].z + face[i - 1].z) / 2, 1.0)

                temp_faces.append([v1, v2, v3, v4])

                if v1 not in self.vertices:
                    self.vertices.append(v1)
                if v2 not in self.vertices:
                    self.vertices.append(v2)
                if v3 not in self.vertices:
                    self.vertices.append(v3)
                if v4 not in self.vertices:
                    self.vertices.append(v4)

        self.faces = temp_faces
        self.subdivision_level += 1

    def remove_subdivision(self):
        if self.subdivision_level != 0:
            temp_faces = []
            for index in range(0, len(self.faces) - 1, 4):
                temp_faces.append([self.faces[index + 0][0], self.faces[index + 1][0], self.faces[index + 2][0],
                                   self.faces[index + 3][0]])
            self.faces = temp_faces
            self.subdivision_level -= 1
        else:
            print("Subdivision level = 0")

    def draw(self):
        count = 0
        for face in self.faces:
            count += 1
            if count % 4 == 1:
                glColor3f(0.0, 0.0, 1.0)
            elif count % 4 == 2:
                glColor3f(0.0, 1.0, 0.0)
            elif count % 4 == 3:
                glColor3f(1.0, 0.0, 0.0)
            else:
                glColor3f(1.0, 1.0, 1.0)
            glBegin(GL_QUADS)
            for vertex in face:
                glVertex3f(vertex.x, vertex.y, vertex.z)
            glEnd()
