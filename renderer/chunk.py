import glm
import numpy as np

from .meshes.chunk_mesh import ChunkMesh
from .world import *


class Chunk:
    def __init__(self, world, position):
        self.app = world.app
        self.world = world
        self.position = position
        self.m_model = self.get_model_matrix()
        self.voxels: np.array = np.zeros((world.chunk_volume, 3), dtype='uint8')
        self.mesh: ChunkMesh = None
        self.is_empty = True
        self.is_dirty = True

    def get_model_matrix(self):
        m_model = glm.translate(glm.mat4(), glm.vec3(self.position) * self.world.chunk_size)
        return m_model

    def set_uniform(self):
        self.mesh.program['model'].write(self.m_model)

    def build_mesh(self):
        self.mesh = ChunkMesh(self)

    def render(self):
        if self.is_dirty:
            if np.any(self.voxels):
                self.is_empty = False
            else:
                self.is_empty = True
            self.is_dirty = False

        if not self.is_empty:
            self.set_uniform()
            self.mesh.render()
