import numpy as np


class GridImporter:
    def __init__(self, array):
        self.array = array

    def initialize(self, app):
        """
             Render a 3D array of voxel data using the VoxelEngine.

             Args:
                 voxel_array (numpy.ndarray): A 4D NumPy array, indexed by x,y,z coordinates, representing the voxel data (rgba).
           """



        len_x, len_y, len_z, len_channels = self.array.shape

        center_x = len_x / 2
        center_z = len_z / 2

        world_x = (8 * 32) / 2
        world_z = (8 * 32) / 2

        for x in range(len_x):
            for y in range(len_y):
                for z in range(len_z):
                    voxel_value = self.array[x, y, z]
                    red, green, blue, alpha = voxel_value
                    color = (red, green, blue)

                    if alpha <= 25:
                        continue

                    # Calculate the offset to center the voxel in the world
                    offset_x = x - center_x

                    offset_z = z - center_z

                    # Calculate the world position for the voxel
                    world_pos_x = world_x + offset_x
                    world_pos_y = y + 5
                    world_pos_z = world_z + offset_z

                    world_pos = (world_pos_x, world_pos_y, world_pos_z)




                    app.scene.world.voxelManager.add_voxel(world_pos, color, False)
                    # print(f"Placing voxel at {world_pos} with col: {color} and alpha {alpha}")
        app.scene.world.voxelManager.rebuild_chunks()
        print("Finished importing grid")
