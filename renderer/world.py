import numpy as np

from .chunk import *
from .chunk import Chunk
from .voxel_manager import *


class World:
    def __init__(self, app, world_dims: tuple[int, int, int] = (8, 8, 8), chunk_size: int = 32,
                 voxel_array: np.ndarray = None):
        self.app = app

        self.chunk_size = chunk_size
        self.half_chunk_size = chunk_size // 2
        self.chunk_area = chunk_size * chunk_size
        self.chunk_volume = self.chunk_area * chunk_size

        if voxel_array is None:
            self.world_width = world_dims[0]
            self.world_height = world_dims[1]
            self.world_depth = world_dims[2]
        else:
            self.world_width = (voxel_array.shape[0] // chunk_size) + 1
            self.world_height = (voxel_array.shape[1] // chunk_size) + 1
            self.world_depth = (voxel_array.shape[2] // chunk_size) + 1
        self.world_area = self.world_width * self.world_depth
        self.world_volume = self.world_area * self.world_height

        self.chunks: list[Chunk] = [None for _ in range(self.world_volume)]
        self.voxelManager = VoxelManager(self)

        self.voxels = np.empty(([self.world_volume, self.chunk_volume, 3]), dtype=np.uint8)

        self.build_chunks(voxel_array)
        self.build_chunk_mesh()

    def build_chunks(self, voxel_array=None):
        for x in range(self.world_width):
            for y in range(self.world_height):
                for z in range(self.world_depth):
                    chunk = Chunk(self, position=(x, y, z))

                    chunk_index = x + self.world_width * z + self.world_area * y
                    self.chunks[chunk_index] = chunk

                    self.voxels[chunk_index] = np.zeros((self.chunk_volume, 3), dtype=np.uint8)

                    if voxel_array is not None:
                        for voxel_x in range(self.chunk_size):
                            for voxel_y in range(self.chunk_size):
                                for voxel_z in range(self.chunk_size):
                                    voxel_index = voxel_x + self.chunk_size * voxel_z + self.chunk_area * voxel_y

                                    # Find the x, y, z coordinates of the portion of voxel_array that correspond to the chunk
                                    chunk_x = x * self.chunk_size + voxel_x
                                    chunk_y = y * self.chunk_size + voxel_y
                                    chunk_z = z * self.chunk_size + voxel_z

                                    # if we are in the bounds of the voxel array
                                    if chunk_x < voxel_array.shape[0] and chunk_y < voxel_array.shape[1] and chunk_z < \
                                            voxel_array.shape[2]:
                                        # overwrite the voxel data in self.voxels with the voxel data from voxel_array
                                        self.voxels[chunk_index][voxel_index] = voxel_array[chunk_x, chunk_y, chunk_z,
                                                                                :3]

                    chunk.voxels = self.voxels[chunk_index]

    def build_chunk_mesh(self):
        for chunk in self.chunks:
            chunk.build_mesh()

    def update(self):
        pass

    def render(self):
        for chunk in self.chunks:
            chunk.render()
