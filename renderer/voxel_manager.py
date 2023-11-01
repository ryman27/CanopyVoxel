import glm

from renderer.meshes.cube_chunk_mesh_builder import get_chunk_index


class VoxelManager:
    def __init__(self, world):
        self.app = world.app
        self.world = world
        self.chunks = world.chunks

    def add_voxel(self, world_pos, color, rebuild=True):
        if color != (0, 0, 0):
            _, voxel_index, _, chunk = self.get_voxel_id(world_pos)

            if isinstance(chunk, int):
                print(f"Invalid world coordinate {world_pos} when trying to place voxel.")
                return

            chunk.voxels[voxel_index] = color

            if chunk.is_empty:
                chunk.is_empty = False

            if rebuild:
                chunk.mesh.rebuild()

    def rebuild_chunks(self):
        for chunk in self.chunks:
            chunk.is_dirty = True
            chunk.mesh.rebuild()

    def remove_voxel(self, world_pos):
        _, voxel_index, voxel_local_pos, chunk = self.get_voxel_id(world_pos)
        chunk.voxels[voxel_index] = (0, 0, 0)

        chunk.mesh.rebuild()
        self.rebuild_adjacent_chunks(chunk.position, voxel_local_pos)

    def rebuild_adj_chunk(self, adj_voxel_pos):
        index = get_chunk_index(adj_voxel_pos, self.world.chunk_size, self.world.world_width, self.world.world_height,
                                self.world.world_depth, self.world.world_area)
        if index != -1:
            self.chunks[index].mesh.rebuild()

    def rebuild_adjacent_chunks(self, world_pos, local_pos):
        wx, wy, wz = world_pos
        lx, ly, lz = local_pos

        if lx == 0:
            self.rebuild_adj_chunk((wx - 1, wy, wz))
        elif lx == self.world.chunk_size - 1:
            self.rebuild_adj_chunk((wx + 1, wy, wz))

        if ly == 0:
            self.rebuild_adj_chunk((wx, wy - 1, wz))
        elif ly == self.world.chunk_size - 1:
            self.rebuild_adj_chunk((wx, wy + 1, wz))

        if lz == 0:
            self.rebuild_adj_chunk((wx, wy, wz - 1))
        elif lz == self.world.chunk_size - 1:
            self.rebuild_adj_chunk((wx, wy, wz + 1))

    def get_voxel_id(self, voxel_world_pos):
        cx, cy, cz = chunk_pos = glm.ivec3(voxel_world_pos) / self.world.chunk_size

        if 0 <= cx < self.world.world_width and 0 <= cy < self.world.world_height and 0 <= cz < self.world.world_depth:
            chunk_index = cx + self.world.world_width * cz + self.world.world_area * cy
            chunk = self.chunks[chunk_index]

            lx, ly, lz = voxel_local_pos = voxel_world_pos - chunk_pos * self.world.chunk_size

            voxel_index = lx + self.world.chunk_size * lz + self.world.chunk_area * ly
            color = chunk.voxels[voxel_index]

            return color, voxel_index, voxel_local_pos, chunk
        else:
            return 0, 0, 0, 0
