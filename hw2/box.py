from vec3d import Vec3d
from Object import Object
from OpenGL.GL import *


class Box(Object):

    def __init__(self):
        Object.__init__(self)
        self.faces = []

    def create(self, length=2):
        # Front
        self.add_vertex(Vec3d(length / 2, length / 2, length / 2, 1.0))  # Top Right
        self.add_vertex(Vec3d(-length / 2, length / 2, length / 2, 1.0))  # Top Left
        self.add_vertex(Vec3d(-length / 2, -length / 2, length / 2, 1.0))  # Bottom Left
        self.add_vertex(Vec3d(length / 2, -length / 2, length / 2, 1.0))  # Bottom Right

        self.faces.append([Vec3d(length / 2, length / 2, length / 2, 1.0),
                           Vec3d(-length / 2, length / 2, length / 2, 1.0),
                           Vec3d(length / 2, -length / 2, length / 2, 1.0),
                           Vec3d(-length / 2, -length / 2, length / 2, 1.0)])
        # Right
        self.add_vertex(Vec3d(length / 2, length / 2, -length / 2, 1.0))
        self.add_vertex(Vec3d(length / 2, length / 2, length / 2, 1.0))
        self.add_vertex(Vec3d(length / 2, -length / 2, length / 2, 1.0))
        self.add_vertex(Vec3d(length / 2, -length / 2, -length / 2, 1.0))

        self.faces.append([Vec3d(length / 2, length / 2, -length / 2, 1.0),
                           Vec3d(length / 2, length / 2, length / 2, 1.0),
                           Vec3d(length / 2, -length / 2, length / 2, 1.0),
                           Vec3d(length / 2, -length / 2, -length / 2, 1.0)])
        # Back
        self.add_vertex(Vec3d(length / 2, length / 2, -length / 2, 1.0))
        self.add_vertex(Vec3d(-length / 2, length / 2, -length / 2, 1.0))
        self.add_vertex(Vec3d(-length / 2, -length / 2, -length / 2, 1.0))
        self.add_vertex(Vec3d(length / 2, -length / 2, -length / 2, 1.0))

        self.faces.append([Vec3d(length / 2, length / 2, -length / 2, 1.0),
                           Vec3d(-length / 2, length / 2, -length / 2, 1.0),
                           Vec3d(-length / 2, -length / 2, -length / 2, 1.0),
                           Vec3d(length / 2, -length / 2, -length / 2, 1.0)])
        # Left
        self.add_vertex(Vec3d(-length / 2, length / 2, -length / 2, 1.0))
        self.add_vertex(Vec3d(-length / 2, length / 2, length / 2, 1.0))
        self.add_vertex(Vec3d(-length / 2, -length / 2, length / 2, 1.0))
        self.add_vertex(Vec3d(-length / 2, -length / 2, -length / 2, 1.0))

        self.faces.append([Vec3d(-length / 2, length / 2, -length / 2, 1.0),
                           Vec3d(-length / 2, length / 2, length / 2, 1.0),
                           Vec3d(-length / 2, -length / 2, length / 2, 1.0),
                           Vec3d(-length / 2, -length / 2, -length / 2, 1.0)])
        # Bottom
        self.add_vertex(Vec3d(length / 2, -length / 2, length / 2, 1.0))
        self.add_vertex(Vec3d(-length / 2, -length / 2, length / 2, 1.0))
        self.add_vertex(Vec3d(-length / 2, -length / 2, -length / 2, 1.0))
        self.add_vertex(Vec3d(length / 2, -length / 2, -length / 2, 1.0))

        self.faces.append([Vec3d(length / 2, -length / 2, length / 2, 1.0),
                           Vec3d(-length / 2, -length / 2, length / 2, 1.0),
                           Vec3d(-length / 2, -length / 2, -length / 2, 1.0),
                           Vec3d(length / 2, -length / 2, -length / 2, 1.0)])
        # Top
        self.add_vertex(Vec3d(length / 2, length / 2, -length / 2, 1.0))
        self.add_vertex(Vec3d(-length / 2, length / 2, -length / 2, 1.0))
        self.add_vertex(Vec3d(-length / 2, length / 2, length / 2, 1.0))
        self.add_vertex(Vec3d(length / 2, length / 2, length / 2, 1.0))

        self.faces.append([Vec3d(length / 2, length / 2, -length / 2, 1.0),
                           Vec3d(-length / 2, length / 2, -length / 2, 1.0),
                           Vec3d(-length / 2, length / 2, length / 2, 1.0),
                           Vec3d(length / 2, length / 2, length / 2, 1.0)])

    def draw(self):
        for face in self.faces:
            glBegin(GL_QUADS)
            glColor3f(0.65, 0.65, 0.65)
            for vertex in face:
                glVertex3f(vertex.x, vertex.y, vertex.z)
            glEnd()
