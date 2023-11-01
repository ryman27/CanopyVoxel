import math
import sys

import numpy as np

import renderer

if __name__ == "__main__":
    print("Load a voxel grid, perform basic operations, and render it.")

    voxel_grid = np.load("data.grid.npy")

    # Calculate grid density
    high_density_count = 0
    total_count = 0

    # normalized_grid = np.zeros_like(voxel_grid)

    normalized_grid = np.zeros(voxel_grid.shape[:-1] + (6,))

    final_grid = np.zeros(voxel_grid.shape[:-1] + (3,))

    # Loop through the voxel grid and accumulate the sums based on density values
    for x in range(voxel_grid.shape[0]):
        for y in range(voxel_grid.shape[1]):
            for z in range(voxel_grid.shape[2]):
                voxel = voxel_grid[x, y, z]

                red = voxel[0]
                green = voxel[1]
                blue = voxel[2]

                intensity = red + green + blue

                if intensity != 0:
                    red_norm = red / intensity
                    green_norm = green / intensity
                    blue_norm = blue / intensity
                else:
                    red_norm = 0
                    green_norm = 0
                    blue_norm = 0

                RGRI = (red - green) / (red + green + np.finfo(float).eps)
                BGRI = (blue - green) / (blue + green + np.finfo(float).eps)

                luminosity = (red + green + blue) / 3

                density = voxel[4]

                if density > 0:
                    total_count += 1
                if density > 0.5:
                    high_density_count += 1

                # Store the calculated values in the new_array at the same index position as voxel
                normalized_grid[x, y, z] = [red_norm, green_norm, blue_norm, RGRI, BGRI, luminosity]

    grid_density = (high_density_count / total_count) * 100

    print(f"Grid density: {grid_density:.2f}%")

    # Now, filter out voxels with low density (channel 4) by multiplying with a mask
    density_mask = voxel_grid[:, :, :, 4] > 0.5
    bgri_mask = normalized_grid[:, :, :, 2] < 0.3
    rgri_mask = normalized_grid[:, :, :, 3] < 0.1
    luminosity_mask = (normalized_grid[:, :, :, 5] > 0.2) & (normalized_grid[:, :, :, 5] < 0.8)

    combined_mask = density_mask  # & bgri & rgri_mask & luminosity_mask  # & blue_mask

    xyz_rgba_voxel_grid = voxel_grid[:, :, :, [0, 1, 2]] * 255 * combined_mask[..., np.newaxis]

    renderer.render_3d_array(xyz_rgba_voxel_grid)
