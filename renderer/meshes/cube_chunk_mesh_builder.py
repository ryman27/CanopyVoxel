import numpy as np

from numba import uint8, njit

from renderer.chunk_helpers import get_chunk_index


class CubeChunkMeshBuilder:
    def __init__(self, world):
        self.world = world

    def build_chunk_mesh(self, chunk_voxels, format_size, chunk_pos, world_voxels):
        return build_chunk_mesh(chunk_voxels, format_size, chunk_pos, world_voxels, self.world.chunk_volume,
                                self.world.chunk_size, self.world.chunk_area, self.world.world_width,
                                self.world.world_height, self.world.world_depth, self.world.world_area)
        pass


@njit
def to_uint8(x, y, z, r, g, b, face_id):
    return uint8(x), uint8(y), uint8(z), uint8(r), uint8(g), uint8(b), uint8(face_id)





@njit
def is_void(local_voxel_pos, world_voxel_pos, world_voxels, chunk_size, chunk_area, world_width, world_height,
            world_depth, world_area):
    chunk_index = get_chunk_index(world_voxel_pos, chunk_size, world_width, world_height, world_depth, world_area)
    if chunk_index == -1:
        return False
    chunk_voxels = world_voxels[chunk_index]

    x, y, z = local_voxel_pos
    voxel_index = x % chunk_size + z % chunk_size * chunk_size + y % chunk_size * chunk_area

    if (chunk_voxels[voxel_index]).any():
        return False
    return True


@njit
def add_data(vertex_data, index, *vertices):
    for vertex in vertices:
        for attr in vertex:
            vertex_data[index] = attr
            index += 1
    return index


@njit
def build_chunk_mesh(chunk_voxels, format_size, chunk_pos, world_voxels, chunk_volume, chunk_size, chunk_area,
                     world_width, world_height, world_depth, world_area):
    vertex_data = np.empty(chunk_volume * 18 * format_size, dtype='uint8')
    index = 0

    for x in range(chunk_size):
        for y in range(chunk_size):
            for z in range(chunk_size):
                color = chunk_voxels[x + chunk_size * z + chunk_area * y]

                r = color[0]
                g = color[1]
                b = color[2]

                if (color == 0).all():
                    continue

                cx, cy, cz = chunk_pos

                wx = x + cx * chunk_size
                wy = y + cy * chunk_size
                wz = z + cz * chunk_size

                # top face
                if is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels, chunk_size, chunk_area, world_width,
                           world_height, world_depth, world_area):
                    # format: x, y, z, r,g,b, face_id
                    v0 = to_uint8(x, y + 1, z, r, g, b, 0)
                    v1 = to_uint8(x + 1, y + 1, z, r, g, b, 0)
                    v2 = to_uint8(x + 1, y + 1, z + 1, r, g, b, 0)
                    v3 = to_uint8(x, y + 1, z + 1, r, g, b, 0)

                    index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)

                # bottom face
                if is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels, chunk_size, chunk_area, world_width,
                           world_height, world_depth, world_area):
                    v0 = to_uint8(x, y, z, r, g, b, 1)
                    v1 = to_uint8(x + 1, y, z, r, g, b, 1)
                    v2 = to_uint8(x + 1, y, z + 1, r, g, b, 1)
                    v3 = to_uint8(x, y, z + 1, r, g, b, 1)

                    index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)

                # right face
                if is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels, chunk_size, chunk_area, world_width,
                           world_height, world_depth, world_area):
                    v0 = to_uint8(x + 1, y, z, r, g, b, 2)
                    v1 = to_uint8(x + 1, y + 1, z, r, g, b, 2)
                    v2 = to_uint8(x + 1, y + 1, z + 1, r, g, b, 2)
                    v3 = to_uint8(x + 1, y, z + 1, r, g, b, 2)

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # left face
                if is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels, chunk_size, chunk_area, world_width,
                           world_height, world_depth, world_area):
                    v0 = to_uint8(x, y, z, r, g, b, 3)
                    v1 = to_uint8(x, y + 1, z, r, g, b, 3)
                    v2 = to_uint8(x, y + 1, z + 1, r, g, b, 3)
                    v3 = to_uint8(x, y, z + 1, r, g, b, 3)

                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

                # back face
                if is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels, chunk_size, chunk_area, world_width,
                           world_height, world_depth, world_area):
                    v0 = to_uint8(x, y, z, r, g, b, 4)
                    v1 = to_uint8(x, y + 1, z, r, g, b, 4)
                    v2 = to_uint8(x + 1, y + 1, z, r, g, b, 4)
                    v3 = to_uint8(x + 1, y, z, r, g, b, 4)

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # front face
                if is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels, chunk_size, chunk_area, world_width,
                           world_height, world_depth, world_area):
                    v0 = to_uint8(x, y, z + 1, r, g, b, 5)
                    v1 = to_uint8(x, y + 1, z + 1, r, g, b, 5)
                    v2 = to_uint8(x + 1, y + 1, z + 1, r, g, b, 5)
                    v3 = to_uint8(x + 1, y, z + 1, r, g, b, 5)

                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

    return vertex_data[:index + 1]
