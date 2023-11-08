import numpy as np
import open3d as o3d

point_cloud_file_name = 'pointcloud_rotated.ply'
qsm_mesh_file_name = 'qsm.ply'

if __name__ == "__main__":
    print("Load a ply point cloud, quantize it to a voxel grid, and save it to disk.")
    pcd = o3d.io.read_point_cloud("pointcloud.ply")

    # Get the point cloud data as a 3D NumPy array
    point_cloud = np.column_stack((pcd.points, pcd.colors))

    print("Points loaded")

    point_cloud_size = np.max(point_cloud[:, :3], axis=0) - np.min(point_cloud[:, :3], axis=0)

    voxel_size_proportion = 0.005

    voxel_size = np.max(point_cloud_size) * voxel_size_proportion

    # Calculate the minimum and maximum bounds for the 3D point cloud
    min_bound = np.min(point_cloud[:, :3], axis=0)
    max_bound = np.max(point_cloud[:, :3], axis=0)

    grid_dimensions = ((max_bound - min_bound) / voxel_size).astype(int) + 1

    # Create an empty voxel grid; each cell has 5 channels.
    # 0,1,2 is RGB info; 3 is count; 4 is relative density
    voxel_grid = np.zeros((grid_dimensions[0], grid_dimensions[1], grid_dimensions[2], 5))

    for point in point_cloud:
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
