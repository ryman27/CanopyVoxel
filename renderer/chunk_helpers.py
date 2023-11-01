from numba import njit


@njit
def get_chunk_index(world_voxel_pos, chunk_size, world_width, world_height, world_depth, world_area):
    wx, wy, wz = world_voxel_pos
    cx = wx // chunk_size
    cy = wy // chunk_size
    cz = wz // chunk_size
    if not (0 <= cx < world_width and 0 <= cy < world_height and 0 <= cz < world_depth):
        return -1

    index = cx + world_width * cz + world_area * cy
    return index