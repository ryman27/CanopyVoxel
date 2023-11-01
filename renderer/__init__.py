import numpy as np

from renderer.addons.plane import plane
from renderer.addons.sphere_demo import Demo
from renderer.voxel_engine import VoxelEngine
from renderer.addons.grid_importer import GridImporter


def render_demo():
    """
       Render a demo scene using the VoxelEngine.
    """

    demo = Demo(64, 64, 64)

    VE = VoxelEngine(custom_update=demo.update)

    # VE.scene.world.enable_demo(True)
    VE.run()


def render_3d_array(array: np.ndarray):
    """
      Render a 3D array of voxel data using the VoxelEngine.

      Args:
          voxel_array (numpy.ndarray): A 4D NumPy array, indexed by x,y,z coordinates, representing the voxel data (rgba).
    """

    # Get the maximum values for each channel
    max_values = np.max(array[:, :, :, :3], axis=(0, 1, 2))

    # Normalize and multiply each channel by 255
    for channel in range(3):
        array[:, :, :, channel] /= max_values[channel]
        array[:, :, :, channel] *= 255

    app = VoxelEngine(voxel_array=array)

    app.run()
