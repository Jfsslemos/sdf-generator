import open3d as o3d
import numpy as np

pcd = o3d.io.read_triangle_mesh("/home/joao/.gazebo/models/obj/meshes/mesh0.obj")
vertices = np.asarray(pcd.vertices)

# Create a point cloud from the mesh vertices
point_cloud = o3d.geometry.PointCloud()
point_cloud.points = o3d.utility.Vector3dVector(vertices)
plane_model, inliers = point_cloud.segment_plane(distance_threshold=0.01, ransac_n=3, num_iterations=1000)
[a, b, c, d] = plane_model
print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")

inlier_cloud = point_cloud.select_by_index(inliers)
inlier_cloud.paint_uniform_color([1.0, 0, 0])
outlier_cloud = point_cloud.select_by_index(inliers, invert=True)
outlier_cloud.paint_uniform_color([0, 0, 1.0])
pointc = inlier_cloud + outlier_cloud
o3d.io.write_point_cloud("point_cloud.ply", pointc)
