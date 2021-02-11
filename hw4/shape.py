from mat3d import Mat3d
from vec3d import Vec3d
import copy
from OpenGL.GL import *

class Shape:

    def __init__(self, vertices, faces):
        self._vertices = vertices
        self._faces = faces
        self._edges = []
        self.create_edge_list()

        self._subdivision_history = []
        self._subdivision_level = 0
        self._size = 0

        self._subdivider = None

        self.transformation_matrix_stack = []
        self.final_transformation_matrix = Mat3d()

    def add_vertex(self, vertex):
        self._vertices.append(vertex)
        self._size += 1

    def remove_vertex(self, vertexnum):
        del self._vertices[vertexnum]

    def add_face(self, vertexnum_list):
        self._faces.append(vertexnum_list)

    def remove_face(self, facenum):
        del self._faces[facenum]

    @property
    def vertices(self):
        return self._vertices

    @vertices.setter
    def vertices(self, vertice_list):
        self._vertices = vertice_list
        self._size = len(self._vertices)
    
    @property
    def faces(self):
        return self._faces

    @faces.setter
    def faces(self, face_list):
        self._faces = face_list

    @property
    def edges(self):
        return self._edges

    @edges.setter
    def edges(self, edge_list):
        self._edges = edge_list

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    def face_number(self):
        return len(self.faces)

    def get_vertex(self, vertexnum):
        return self.vertices[vertexnum].copy()
        
    def get_face(self, facenum):
        return copy.copy(self.faces[facenum])

    def get_edge(self, edgenum):
        return copy.copy(self.edges[edgenum])

    def reset(self):
        self.vertices = []
        self.faces = []
        self.size = 0

    def transform_shape(self, a_mat3d):
        """ 
        Perform transformation
        """
        for i in range(len(self.vertices)):
            self.vertices[i] = a_mat3d.vecmul(self.vertices[i])
        return self

    def add_transformation(self, a_mat3d):
        """ 
        Adds transformation matrix to the matrix stack and multiply matrix with other transformations.
        """
        if len(self.transformation_matrix_stack) == 0:
            self.final_transformation_matrix = a_mat3d
        else:
            self.final_transformation_matrix = a_mat3d.matmul(self.final_transformation_matrix)
        self.transformation_matrix_stack.append(a_mat3d)
        return self

    def get_final_transformation_matrix(self):
        """ 
        Returns final transformation matrix.
        """
        return self.final_transformation_matrix

    def add_subdivision(self):
        temp_faces = []
        for face in self.faces:
            index = self.size
            # center vertice of face
            center = Vec3d((self.vertices[face[0]].x + self.vertices[face[2]].x) / 2,
                            (self.vertices[face[0]].y + self.vertices[face[2]].y) / 2,
                            (self.vertices[face[0]].z + self.vertices[face[2]].z) / 2, 1.0)
            self.vertices.append(center)
            center_index = index
            
            # then split each edge in half
            v1 = Vec3d((self.vertices[face[0]].x + self.vertices[face[1]].x) / 2,
                        (self.vertices[face[0]].y + self.vertices[face[1]].y) / 2,
                        (self.vertices[face[0]].z + self.vertices[face[1]].z) / 2, 1.0)
            self.vertices.append(v1)
            v1_index = index + 1

            v2 = Vec3d((self.vertices[face[1]].x + self.vertices[face[2]].x) / 2,
                        (self.vertices[face[1]].y + self.vertices[face[2]].y) / 2,
                        (self.vertices[face[1]].z + self.vertices[face[2]].z) / 2, 1.0)
            self.vertices.append(v2)
            v2_index = index + 2

            v3 = Vec3d((self.vertices[face[2]].x + self.vertices[face[3]].x) / 2,
                        (self.vertices[face[2]].y + self.vertices[face[3]].y) / 2,
                        (self.vertices[face[2]].z + self.vertices[face[3]].z) / 2, 1.0)
            self.vertices.append(v3)
            v3_index = index + 3

            v4 = Vec3d((self.vertices[face[3]].x + self.vertices[face[0]].x) / 2,
                        (self.vertices[face[3]].y + self.vertices[face[0]].y) / 2,
                        (self.vertices[face[3]].z + self.vertices[face[0]].z) / 2, 1.0)
            self.vertices.append(v4)
            v4_index = index + 4

            self.size += 5

            # 4 faces occur for 1 face and we add these 4 faces to new face list.
            face_list = [[v1_index, face[1], v2_index, center_index],
                        [v2_index, face[2], v3_index, center_index],
                        [v3_index, face[3], v4_index, center_index],
                        [v4_index, face[0], v1_index, center_index]]
            
            temp_faces += face_list

        self._subdivision_history.append(self.faces)
        self.faces = temp_faces
        self._subdivision_level += 1

    def remove_subdivision(self):
        if len(self._subdivision_history) != 0:
            self.faces = self._subdivision_history.pop()
            self._subdivision_level -= 1
        else:
            print("Subdivision level = 0")

    def draw_lines(self):
        for face in self.faces:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glLineWidth(2)
            glBegin(GL_POLYGON)
            glColor3f(0, 0, 0)
            for vertex in face:
                vertice = self.vertices[vertex]
                glVertex3f(vertice.x, vertice.y, vertice.z)
            glEnd()
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def draw(self):
        for face in self.faces:
            glColor3f(0.65, 0.65, 0.65)
            glBegin(GL_POLYGON)
            for vertex in face:
                vertice = self._vertices[vertex]
                glVertex3f(vertice.x, vertice.y, vertice.z)
            glEnd()

    def face_to_vertices(self, facenum):
        """
         Find vertices in face for given face index.

        """
        return self.faces[facenum]

    def face_to_edges(self, facenum):
        """
        Find edge indexes in face for given face index
        """
        edge_nums = []
        # find face
        face = self.faces[facenum]
        # create edges for face
        edges = self.create_edges(face)
        for edge in edges:
            # looking for same edge in edge list. 
            edge_num = self.find_edge_num(edge)
            # append the index of edge.
            edge_nums.append(edge_num)
        return edge_nums

    def vertex_to_faces(self, vertexnum):
        """
        Find out which face given vertex is in.
        """
        face_nums = []

        counter = 0
        for face in self.faces:
            if(vertexnum in face):
                 # if vertex index is in face, append face index.
                face_nums.append(counter)
            # vertex index is not in the face, increase face index.
            counter += 1
        # return face indexes.
        return face_nums

    def vertex_to_edges(self, vertexnum):
        """
        Find out which edge given vertex is in.
        """
        edge_nums = []

        counter = 0
        for edge in self.edges:
            if(vertexnum in edge):
                # if vertex is in edge, append edge index.
                edge_nums.append(counter)
            # vertex index is not in the edge, increase edge index.
            counter += 1
        # return edge indexes.
        return edge_nums

    def edge_to_vertices(self, edgenum):
        """
        Find vertices in the given edge.
        """
        return self.edges[edgenum]

    def edge_to_faces(self, edgenum):
        """
        Find out which face given edge is in.
        """
        faces = []

        for facenum in range(len(self.faces)):
            # find edge indexes for each face.
            edges = self.face_to_edges(facenum)
            if(edgenum in edges):
                # if given edge index is equal to one of the indexes, append face index.
                faces.append(facenum)
        # return face indexes.
        return faces

    def create_edge_list(self):
        """
        Creates edge list.
        """
        for face in self.faces:
            # for each face create edges.
            edges = self.create_edges(face)
            for edge in edges:
                # for each edge add to the list.
                self.add_edge(edge)
        
    def create_edges(self, face):
        """
        Create edges for the given face.
        """
        edges = []

        index = [-1, 0, 1, 2]
        for i in index:
            edge = []
            edge.append(face[i])
            edge.append(face[i + 1])

            edges.append(edge)
        
        return edges

    def add_edge(self, edge):
        """
        Add given edge to the edge list.
        """
        if(self.is_edge_exist(edge) != True):
            # if edge is not exist, add to the list.
            self.edges.append(edge)

    def is_edge_exist(self, edge):
        """
        Check if edge is exist.
        """
        if(self.find_edge_num(edge) != None):
            return True
    
        return False

    def find_edge_num(self, edge):
        """
        Find index of given edge in edge list.
        """
        counter = 0
        for e in self.edges:
            # looking for the same edge.
            if(edge[0] == e[0] and edge[1] == e[1]):
                return counter
            
            if(edge[0] == e[1] and edge[1] == e[0]):
                return counter
            # increase the index.
            counter += 1
        # if could not find, return None.
        return None

    def update_shape(self, vertices, faces):
        """
        Update shape with given vertices and faces.
        """
        self.vertices = vertices
        self.faces = faces
        self.edges = []
        self.size = len(vertices)
        
        self.create_edge_list()
