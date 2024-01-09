import numpy as np

from .bin import voxelTest as vt
from .bin.voxelTest import voxelWindow

coordinate = vt.coordinate
hsv = vt.hsv
rgb = vt.rgb
rgba = vt.rgba


def create_voxel_window(chunk_length: int, chunk_size: int, window_width: int, window_height: int,
                        background_color: vt.rgba = vt.rgba(0.2, 0.1, 0.1, 1), custom_update=None):
    vw = vt.voxelWindow(chunk_length, chunk_size, window_width, window_height, background_color)

    vw.updates = []

    if custom_update is not None:
        vw.updates.append(custom_update)

    # Store the original update method
    original_update = vw.update

    # Define a new update method
    def patched_update():
        # Call all functions in the updates list
        for func in vw.updates:
            func(vw)

        original_update()

    # Replace the original update method with the patched one
    vw.update = patched_update

    return vw


def render_3d_array(array: np.ndarray):
    len_x, len_y, len_z, len_channels = array.shape

    center_x = len_x / 2
    center_z = len_z / 2

    world_x = int((8 * 32) / 2)
    world_z = int((8 * 32) / 2)

    voxel_renderer = vt.voxelWindow(16, 32, 1200, 900, vt.rgba(0, 0, 0, 1))

    for x in range(len_x):
        for y in range(len_y):
            for z in range(len_z):
                voxel_value = array[x, y, z]
                red, green, blue = voxel_value
                color = vt.rgba(red, green, blue, 1)

                # Calculate the offset to center the voxel in the world
                offset_x = x - center_x

                offset_z = z - center_z

                # Calculate the world position for the voxel
                world_pos_x = int(world_x + offset_x)
                world_pos_y = y + 5
                world_pos_z = int(world_z + offset_z)

                world_pos = vt.coordinate(world_pos_x, world_pos_y, world_pos_z)

                voxel_renderer.SetVoxel(world_pos, color)

    while not voxel_renderer.ShouldClose():
        voxel_renderer.update()
