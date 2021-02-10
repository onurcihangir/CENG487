from Object import Object
import math
from vec3d import Vec3d
from OpenGL.GL import *


class Cylinder(Object):

    def __init__(self):
        Object.__init__(self)
        self.faces = []
        self.angle = 0

    def create(self, radius=1, length=2, angle=30):
        self.angle = angle
        step_angle = angle

        while step_angle <= 360:
            face = []
            a, b = self.angle_to_coords(step_angle, radius)
            step_angle += angle
            c, d = self.angle_to_coords(step_angle, radius)
            self.add_vertex(Vec3d(a, length / 2, b, 1))
            self.add_vertex(Vec3d(c, length / 2, d, 1))
            self.add_vertex(Vec3d(c, -length / 2, d, 1))
            self.add_vertex(Vec3d(a, -length / 2, b, 1))
            face.append(Vec3d(a, length / 2, b, 1))
            face.append(Vec3d(c, length / 2, d, 1))
            face.append(Vec3d(c, -length / 2, d, 1))
            face.append(Vec3d(a, -length / 2, b, 1))
            self.faces.append(face)

    def angle_to_coords(self, theta, radius):
        theta_radian = self.calculate_radian(theta)
        x = math.cos(theta_radian) * radius
        z = math.sin(theta_radian) * radius
        return x, z

    @staticmethod
    def calculate_radian(degree):
        return degree * (math.pi / 180)

    def draw(self):
        for face in self.faces:
            glBegin(GL_QUADS)
            glColor3f(0.65, 0.65, 0.65)
            for vertex in face:
                glVertex3f(vertex.x, vertex.y, vertex.z)
            glEnd()

    def add_subdivision(self):
        self.faces = []
        self.vertices = []
        self.original_vertices = []
        self.angle /= 2
        self.create(angle=self.angle)

    def remove_subdivision(self):
        self.angle *= 2
        if self.angle <= 120:
            self.faces = []
            self.vertices = []
            self.original_vertices = []
            self.create(angle=self.angle)
        else:
            print("Limit!!")
            self.angle /= 2
