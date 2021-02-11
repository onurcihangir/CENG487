from shape import Shape
from vec3d import Vec3d

class CatmullClark():

    def __init__(self, shape):
        self._shape = shape

        self._vertices = []
        self._faces = []

        self._face_point = {}
        self._edge_point = {}
        self._vertex_point = {}

        self._subdivision_history = []

    def add_vertex(self, vertex):
        index = len(self._vertices)
        self._vertices.append(vertex)

        return index

    def get_vertex(self, vertex_num):
        return self._vertices[vertex_num].copy()

    def add_history(self):
        self._subdivision_history.append(self._shape.faces)
        self._subdivision_history.append(self._shape.vertices)

    def remove_subdivision(self):
        if(len(self._subdivision_history) != 0):
            vertices = self._subdivision_history.pop()
            faces = self._subdivision_history.pop()
            self._shape.update_shape(vertices, faces)
            self._shape._subdivision_level -= 1
        else:
            print("Subdivision level = 0")
        self.reset()

    def reset(self):
        self._vertices = []
        self._faces = []

        self._face_point = {}
        self._edge_point = {}
        self._vertex_point = {}

    def add_subdivision(self):
        shape = self._shape
        
        self.add_history()

        face_count = shape.face_number()
        for facenum in range(face_count):
            divided_faces = self.subdivide_face(facenum)
            self._faces += divided_faces

        self._shape.update_shape(self._vertices, self._faces)
        self._shape._subdivision_level += 1
        self.reset()

    def subdivide_face(self, facenum):
        """
        Subdivide face which is given its index.
        """
   
        # all has references to self._vertices
        face_point = self.calculate_face_point(facenum)
        edge_points = []
        vertex_points = []

        # find edges for given face.
        edge_nums = self._shape.face_to_edges(facenum)
        for edgenum in edge_nums:
            # calculate each edge point for face's edges and append their indexes to the list.
            edge_point = self.calculate_edge_point(edgenum)
            edge_points.append(edge_point)

        # find vertices for given face. 
        vertex_nums = self._shape.face_to_vertices(facenum)
        for vertexnum in vertex_nums:
            # calculate each vertex point for face's vertices and append their indexes to the list.
            vertex_point = self.calculate_vertex_point(vertexnum)
            vertex_points.append(vertex_point)

        # connect them.
        divided_faces = self.connect_quad(face_point, edge_points, vertex_points)

        return divided_faces

    def connect_quad(self, face_point, edge_points, vertex_points):
        """
        Connect given points (indexes) and return 4 new faces.
        """
        divided_faces = []

        f0 = [vertex_points[3], edge_points[0], face_point, edge_points[3]]
        f1 = [vertex_points[0], edge_points[1], face_point, edge_points[0]]
        f2 = [vertex_points[2], edge_points[3], face_point, edge_points[2]]
        f3 = [vertex_points[1], edge_points[2], face_point, edge_points[1]]
    
        divided_faces.append(f0)
        divided_faces.append(f1)
        divided_faces.append(f2)
        divided_faces.append(f3)

        return divided_faces

    def calculate_face_point(self, facenum):
        """
        Calculate face point for given face index.
        """
        # if calculate it before, return it.
        if(facenum in self._face_point):
            return self._face_point[facenum]

        average_list = []
        # get vertices in the face.
        vertices = self._shape.face_to_vertices(facenum)
        for vertexnum in vertices:
            vertex = self._shape.get_vertex(vertexnum)
            average_list.append(vertex)
        # calculate average of them and find face point.
        face_point = self.calculate_average_vertices(average_list)
        # append face point to the vertex list and append its index to the face point list.
        index = self.add_vertex(face_point)
        self._face_point[facenum] = index
        
        return index

    def calculate_edge_point(self, edgenum):
        """
        Calculate edge point for given edge index.
        """
        # if calculate it before, return it.
        if(edgenum in self._edge_point):
            return self._edge_point[edgenum]

        average_list = []

        # find vertices in edge for given edge index.
        vertex_nums = self._shape.edge_to_vertices(edgenum)
        for vertexnum in vertex_nums:
            # for vertex index, find vertex and append in a list.
            vertex = self._shape.get_vertex(vertexnum)
            average_list.append(vertex)
        # find face indexes to which the edge belongs.
        face_nums = self._shape.edge_to_faces(edgenum)
        for facenum in face_nums:
            # calculate facepoints for each face and get their indexes.
            vertex_num = self.calculate_face_point(facenum)
            # get facepoints and append in a list.
            average_list.append(self.get_vertex(vertex_num))
        # calculate average of them and find edge point.
        edge_point = self.calculate_average_vertices(average_list)
        # append edge point to the vertex list and append its index to the edge point list.
        index = self.add_vertex(edge_point)
        self._edge_point[edgenum] = index

        return index

    def calculate_vertex_point(self, vertex_num):
        """
        Calculate new coordinates for given vertex index.
        """
        # if calculate it before, return it.
        if(vertex_num in self._vertex_point):
            return self._vertex_point[vertex_num]

        vertex_point = Vec3d(0,0,0,1.0)

        n = 3 
        f = self.calculate_F(vertex_num)
        r = self.calculate_R(vertex_num)

        # (F + 2R + P(n - 3)) / n
        # P is multiplied by (3 - 3) so it is ineffective.

        vertex_point += f
        r2 = Vec3d(r.x * 2, r.y * 2, r.z * 2, 1.0)
        vertex_point += r2
        vertex_point2 = Vec3d(vertex_point.x / n, vertex_point.y / n, vertex_point.z / n, 1.0)

        # add new point to the vertex list and return its index.
        index = self.add_vertex(vertex_point2)
        # add index of new point.
        self._vertex_point[vertex_num] = index

        return index

    def calculate_F(self, vertex_num):
        """
        Calculate average of all face points for faces touching vertex.
        """
        
        average_list = []

        # find face indexes which is touching vertex.
        face_nums = self._shape.vertex_to_faces(vertex_num)
        for facenum in face_nums:
            # calculate each facepoint for faces and store its index.
            face_point_num = self.calculate_face_point(facenum)
            # find facepoint in vertex list and append in a list.
            average_list.append(self.get_vertex(face_point_num))
        # calculate average of facepoints.
        q = self.calculate_average_vertices(average_list)

        return q

    def calculate_R(self, vertex_num):
        """
        Calculate average of all edge midpoints for edges touching vertex.
        """

        average_list = []

        # find edge indexes which is touching vertex. 
        edge_nums = self._shape.vertex_to_edges(vertex_num)
        for edgenum in edge_nums:
            # calculate each midpoints for edges and append in a list.
            midpoint = self.calculate_edge_midpoint(edgenum)
            average_list.append(midpoint)
        # calculate average of edge midpoints.
        r = self.calculate_average_vertices(average_list)

        return r

    def calculate_edge_midpoint(self, edge_num):
        """
        Calculate edge midpoints for given edge index.
        """

        average_list = []

        # get vertex indexes for given edge index.
        vertex_nums = self._shape.get_edge(edge_num)
        for vertexnum in vertex_nums:
            # get vertices for vertex indexes in edge.
            vertex = self._shape.get_vertex(vertexnum)
            average_list.append(vertex)

        # # calculate their average.
        midpoint = self.calculate_average_vertices(average_list)

        return midpoint

    def calculate_average_vertices(self, vertex_list):
        """
        Calculate average for given vertices.
        """
        counter = 0
        average = Vec3d(0, 0, 0, 1.0)
        for vertex in vertex_list:
            # sum each vertex.
            average.x += vertex.x
            average.y += vertex.y
            average.z += vertex.z
            counter += 1
        # divide by number of vertices.
        average.x /= counter
        average.y /= counter
        average.z /= counter
        return average

    