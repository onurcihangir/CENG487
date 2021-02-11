from vec3d import Vec3d
import sys

class ObjParser:

    @staticmethod
    def parse():
        vertices = []
        faces = []
        with open(sys.argv[1], 'r') as f:
            for line in f:
                if line.startswith('v'):
                    values = line.split()
                    vertex = Vec3d(float(values[1]), float(values[2]), float(values[3]), 1.0)
                    vertices.append(vertex)
                elif line.startswith('f'):
                    values = line.split()
                    face = []
                    for i in values[1:]:
                        face.append(int(i) - 1)
                    faces.append(face)
        return vertices, faces
