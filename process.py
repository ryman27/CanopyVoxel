import numpy as np
from pyntcloud import PyntCloud
from tqdm import tqdm

point_cloud_file_name = 'pointcloud_rotated.ply'
qsm_mesh_file_name = 'qsm.ply'

if __name__ == "__main__":
    print("Load a ply point cloud, quantize it to a voxel grid, and save it to disk.")
    pynt_cloud = PyntCloud.from_file(point_cloud_file_name)

    # Get the point cloud data as a 3D NumPy array
    points = pynt_cloud.points[['x', 'y', 'z']].values
    colors = pynt_cloud.points[['red', 'green', 'blue']].values / 255.0  # Normalize color values

    point_cloud = np.column_stack((points, colors))

    print("Points loaded")

    point_cloud_size = np.max(points, axis=0) - np.min(points, axis=0)

    voxel_size_proportion = 0.01  # Make this smaller to increase the resolution of the voxel grid. Make it larger to decrease the resolution. 0.01 is a good starting point.

    voxel_size = np.max(point_cloud_size) * voxel_size_proportion

    # Calculate the minimum and maximum bounds for the 3D point cloud
    min_bound = np.min(point_cloud[:, :3], axis=0)
    max_bound = np.max(point_cloud[:, :3], axis=0)

    grid_dimensions = ((max_bound - min_bound) / voxel_size).astype(int) + 1

    # Create an empty voxel grid; each cell has 5 channels.
    # 0,1,2 is RGB info; 3 is count; 4 is relative density
    voxel_grid = np.zeros((grid_dimensions[0], grid_dimensions[1], grid_dimensions[2], 5))

    # Assuming point_cloud is a list or iterable of points
    for point in tqdm(point_cloud, desc="Processing Points"):
        # Calculate the voxel index for each point
        voxel_index = ((point[:3] - min_bound) / voxel_size).astype(int)

        # Extract the voxel color (R, G, B) from the point's last three elements
        color = point[3:]

        # Update voxel count and accumulate color
        voxel_grid[voxel_index[0], voxel_index[1], voxel_index[2], 0:3] += color  # Accumulate color
        voxel_grid[voxel_index[0], voxel_index[1], voxel_index[2], 3] += 1  # Count

    # Calculate the mask for nonzero counts
    nonzero_count_mask = voxel_grid[..., 3] != 0

    nonzero_counts = voxel_grid[nonzero_count_mask, 3]

    nonzero_total = np.where(nonzero_count_mask, voxel_grid[..., 3], 1)

    percentile_90 = np.percentile(nonzero_counts, 90)

    voxel_grid[..., 0:3] /= nonzero_total[..., np.newaxis]
    voxel_grid[..., 4] = np.minimum(voxel_grid[..., 3] / percentile_90, 1)

    np.save("large-data.grid", voxel_grid)

    print("Voxel grid saved")
