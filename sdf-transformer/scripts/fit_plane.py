import open3d as o3d
import numpy as np
from copy import deepcopy
EPS = np.finfo(float).eps   # smallest possible difference

def rotation_matrix_a_to_b(A, B):
    cos = np.dot(A, B)
    sin = np.linalg.norm(np.cross(B, A))
    u = A
    v = B - np.dot(A, B) * A
    v = v / (np.linalg.norm(v) + EPS)
    w = np.cross(B, A)
    w = w / (np.linalg.norm(w) + EPS)
    F = np.stack([u, v, w], 1)
    G = np.array([[cos, -sin, 0],
                [sin, cos, 0],
                [0, 0, 1]])
    # B = R @ A
    try:
        R = F @ G @ np.linalg.inv(F)
    except:
        R = np.eye(3, dtype=np.float32)
    return R

# Load mesh from file
mesh = o3d.io.read_triangle_mesh("/home/joao/.gazebo/models/obj/meshes/mesh0.obj")  # Replace with the path to your mesh file

vertices = np.asarray(mesh.vertices)

# Create a point cloud from the mesh vertices
point_cloud = o3d.geometry.PointCloud()
point_cloud.points = o3d.utility.Vector3dVector(vertices)


points = np.asarray(point_cloud.points)

# Use RANSAC to fit a plane
plane_model, inliers = point_cloud.segment_plane(distance_threshold=0.01, ransac_n=3, num_iterations=1000)
R = rotation_matrix_a_to_b(plane_model[:3], np.array([0, 0, 1]))
mesh_new = deepcopy(mesh)
mesh_new.rotate(R, center=mesh.get_center()).translate((0,0,-plane_model[3]))
o3d.io.write_triangle_mesh('mesh0.obj', mesh_new)
o3d.visualization.draw_geometries([mesh, mesh_new])