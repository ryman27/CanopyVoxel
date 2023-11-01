import math

import glm

from .world import *


class Camera:

    def __init__(self, position, yaw, pitch, fov=50, resolution=glm.vec2(1600, 900)):
        self.position = glm.vec3(position)
        self.yaw = glm.radians(yaw)
        self.pitch = glm.radians(pitch)
        self.max_pitch = glm.radians(89)

        self.vec3_up = glm.vec3(0, 1, 0)
        self.vec3_right = glm.vec3(1, 0, 0)
        self.vec3_forward = glm.vec3(0, 0, -1)

        self.fov_degrees = fov

        self.near_clipping = 0.1
        self.far_clipping = 2000.0

        self.view_matrix = glm.fmat4x4
        self.projection_matrix = glm.mat4()

        self.refresh(resolution)

    def refresh(self, resolution=glm.vec2(1600, 900)):
        vertical_fov = glm.radians(self.fov_degrees)  # vertical FOV
        aspect_ratio = resolution.x / resolution.y

        self.projection_matrix = glm.perspective(vertical_fov, aspect_ratio, self.near_clipping,
                                                 self.far_clipping)
        self.view_matrix = glm.mat4()

    def update(self, app):
        self.update_relative_vectors()
        self.update_view_matrix()

    def update_view_matrix(self):
        self.view_matrix = glm.lookAt(self.position, self.position + self.vec3_forward, self.vec3_up)

    def update_relative_vectors(self):
        self.vec3_forward.x = glm.cos(self.yaw) * glm.cos(self.pitch)
        self.vec3_forward.y = glm.sin(self.pitch)
        self.vec3_forward.z = glm.sin(self.yaw) * glm.cos(self.pitch)

        self.vec3_forward = glm.normalize(self.vec3_forward)
        self.vec3_right = glm.normalize(glm.cross(self.vec3_forward, glm.vec3(0, 1, 0)))
        self.vec3_up = glm.normalize(glm.cross(self.vec3_right, self.vec3_forward))

    def rotate_pitch(self, delta_y):
        self.pitch -= delta_y
        self.pitch = glm.clamp(self.pitch, -self.max_pitch, self.max_pitch)

    def rotate_yaw(self, delta_x):
        self.yaw += delta_x
