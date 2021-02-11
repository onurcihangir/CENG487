from vec3d import Vec3d
from mat3d import Mat3d


class Camera:
    def __init__(self):
        self.eye = Vec3d(0.0, 0.0, 0.0, 1.0)
        self.center = Vec3d(0.0, 0.0, 0.0, 1.0)
        self.up = Vec3d(0.0, 0.0, 0.0, 0.0)

        self.original_eye = Vec3d(0.0, 0.0, 0.0, 1.0)
        self.original_center = Vec3d(0.0, 0.0, 0.0, 1.0)
        self.original_up = Vec3d(0.0, 0.0, 0.0, 1.0)

        self.cameraX = Vec3d(0.0, 0.0, 0.0, 0.0)
        self.cameraY = Vec3d(0.0, 0.0, 0.0, 0.0)
        self.cameraZ = Vec3d(0.0, 0.0, 0.0, 0.0)

        self.create_view(Vec3d(2.0, 3.0, 5.0, 1.0),
                         Vec3d(0.0, 0.0, 0.0, 1.0),
                         Vec3d(0.0, 1.0, 0.0, 0.0))

    def create_view(self, eye_point, center_point, up_vector):
        self.eye = eye_point
        self.original_eye = eye_point

        self.center = center_point
        self.original_center = center_point

        self.up = up_vector
        self.original_up = up_vector

        self.compute_camera_space()

    def compute_camera_space(self):
        self.cameraZ = self.eye - self.center
        self.cameraZ = self.cameraZ.normalize()

        self.cameraX = self.up.cross_product(self.cameraZ)
        self.cameraX = self.cameraX.normalize()

        self.cameraY = self.cameraZ.cross_product(self.cameraX)

    def rotate(self, yaw_angle, pitch_angle):
        cam_focus_vector = Vec3d(self.eye.x - self.center.x, self.eye.y - self.center.y, self.eye.z - self.center.z,
                                 1.0)
        ymat = Mat3d()
        pmat = Mat3d()
        ymat.define_rotation_matrix(yaw_angle, "y")
        pmat.define_rotation_matrix(pitch_angle, "x")
        ymat.matmul(pmat)
        cam_focus_vector = ymat.vecmul(cam_focus_vector)
        cam_focus_vector += self.center
        self.eye = cam_focus_vector

        self.compute_camera_space()

    def reset(self):
        self.eye = self.original_eye
        self.center = self.original_center
        self.up = self.original_up
        self.compute_camera_space()
