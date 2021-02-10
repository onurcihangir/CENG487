from vec3d import Vec3d
from Object import Object
from OpenGL.GL import *


class Pyramid(Object):

    def __init__(self):
        Object.__init__(self)
        self.faces = []

    def create(self):
        # Bottom
        self.add_vertex(Vec3d(-1.0, -1.0, -1.0, 1.0))
        self.add_vertex(Vec3d(-1.0, -1.0, 1.0, 1.0))
        self.add_vertex(Vec3d(1.0, -1.0, 1.0, 1.0))
        self.add_vertex(Vec3d(1.0, -1.0, -1.0, 1.0))

        self.faces.append([Vec3d(-1.0, -1.0, -1.0, 1.0),
                           Vec3d(-1.0, -1.0, 1.0, 1.0),
                           Vec3d(1.0, -1.0, 1.0, 1.0),
                           Vec3d(1.0, -1.0, -1.0, 1.0)])
        # Front
        self.add_vertex(Vec3d(-1.0, -1.0, -1.0, 1.0))
        self.add_vertex(Vec3d(1.0, -1.0, -1.0, 1.0))
        self.add_vertex(Vec3d(0.0, 1.0, 0.0, 1.0))

        self.faces.append([Vec3d(-1.0, -1.0, -1.0, 1.0),
                           Vec3d(-1.0, -1.0, 1.0, 1.0),
                           Vec3d(0.0, 1.0, 0.0, 1.0)])
        # Left
        self.add_vertex(Vec3d(-1.0, -1.0, -1.0, 1.0))
        self.add_vertex(Vec3d(-1.0, -1.0, 1.0, 1.0))
        self.add_vertex(Vec3d(0.0, 1.0, 0, 1.0))

        self.faces.append([Vec3d(-1.0, -1.0, 1.0, 1.0),
                           Vec3d(1.0, -1.0, 1.0, 1.0),
                           Vec3d(0.0, 1.0, 0.0, 1.0)])
        # Right
        self.add_vertex(Vec3d(1.0, -1.0, 1.0, 1.0))
        self.add_vertex(Vec3d(1.0, -1.0, -1.0, 1.0))
        self.add_vertex(Vec3d(0.0, 1.0, 0.0, 1.0))

        self.faces.append([Vec3d(1.0, -1.0, 1.0, 1.0),
                           Vec3d(1.0, -1.0, -1.0, 1.0),
                           Vec3d(0.0, 1.0, 0.0, 1.0)])
        # Back
        self.add_vertex(Vec3d(-1.0, -1.0, 1.0, 1.0))
        self.add_vertex(Vec3d(1.0, -1.0, 1.0, 1.0))
        self.add_vertex(Vec3d(0.0, 1.0, 0.0, 1.0))

        self.faces.append([Vec3d(-1.0, -1.0, 1.0, 1.0),
                           Vec3d(1.0, -1.0, 1.0, 1.0),
                           Vec3d(0.0, 1.0, 0.0, 1.0)])

    def draw(self, red, green, blue):
        for face in self.faces:
            glBegin(GL_POLYGON)
            glColor3f(red, green, blue)
            for vertex in face:
                glVertex3f(vertex.x, vertex.y, vertex.z)
            glEnd()
