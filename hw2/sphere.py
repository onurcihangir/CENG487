from Object import Object
from vec3d import Vec3d
import math
from OpenGL.GL import *


class Sphere(Object):

    def __init__(self):
        Object.__init__(self)
        self.faces = []
        self.angle = 0

    def create(self, angle=30, radius=1):
        self.angle = angle
        phi = theta = angle
        phi_step = theta_step = 0

        while theta_step <= 180:
            while phi_step <= 360:
                face = []
                x1, y1, z1 = self.angle_to_coords(theta_step, phi_step, radius)
                phi_step += phi
                x2, y2, z2 = self.angle_to_coords(theta_step, phi_step, radius)
                theta_step += theta
                x3, y3, z3 = self.angle_to_coords(theta_step, phi_step, radius)
                x4, y4, z4 = self.angle_to_coords(theta_step, phi_step - phi, radius)
                theta_step -= theta
                self.add_vertex(Vec3d(x1, y1, z1, 1))
                self.add_vertex(Vec3d(x2, y2, z2, 1))
                self.add_vertex(Vec3d(x3, y3, z3, 1))
                self.add_vertex(Vec3d(x4, y4, z4, 1))
                face.append(Vec3d(x1, y1, z1, 1))
                face.append(Vec3d(x2, y2, z2, 1))
                face.append(Vec3d(x3, y3, z3, 1))
                face.append(Vec3d(x4, y4, z4, 1))
                self.faces.append(face)
            phi_step = 0
            theta_step += theta

    def angle_to_coords(self, theta, phi, radius):
        phi_radian = self.calculate_radian(phi)
        theta_radian = self.calculate_radian(theta)
        x = radius * math.sin(theta_radian) * math.cos(phi_radian)
        y = radius * math.sin(theta_radian) * math.sin(phi_radian)
        z = radius * math.cos(theta_radian)

        return x, y, z

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
