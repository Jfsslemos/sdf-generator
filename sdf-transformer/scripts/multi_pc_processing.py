# examples/Python/Basic/pointcloud.py
###
### TODO ::: uri of the meshes keeps getting as the local directory instead of the gazebo directory
###
import numpy as np
import open3d as o3d
from sdf_writer import create_xml
from move_files import create_gazebo_dir
from multi_sdf_writer import create_single_xml
import os
from copy import deepcopy

EPS = np.finfo(float).eps   # smallest possible difference

def transform_mesh(mesh):
    vertices = np.asarray(mesh.vertices)

    # Create a point cloud from the mesh vertices
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(vertices)

    # Use RANSAC to fit a plane
    plane_model, _ = point_cloud.segment_plane(distance_threshold=0.01, ransac_n=3, num_iterations=1000)
    R = rotation_matrix_a_to_b(plane_model[:3], np.array([0, 0, 1]))
    return R, plane_model, mesh.get_center()

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

def mesh_and_sdf_creation():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    mesh_color_uns = {}
    mesh_nro = 0
    new_vertices = []
    mesh_by_color_dict = {}
    mesh_colors=[]
    xml_infos_dict = {
        'model_name': [],
        'mesh_uri':[],
        'collision_scale':[],
        'mesh_color':[]
    }
    mesh = o3d.io.read_triangle_mesh("/home/joao/study/202208282311/mesh_430000/color_study.ply")
    vertex_colors = mesh.vertex_colors

    for idx, color in enumerate(vertex_colors):
        #function to make the color hashable
        scaled_values = [int(value * 255) for value in np.asarray(color)]
        result_integer = str(''.join(map(str, scaled_values)))

        uns_scaled_values = [float(value) for value in np.asarray(color)]
        uns_result_integer = str(''.join(map(str, uns_scaled_values)))

        #function to set a mesh name for each instance color 
        if result_integer not in list(mesh_by_color_dict.keys()):
            mesh_color_uns[uns_result_integer] = [idx]
            mesh_by_color_dict[result_integer] = [idx]

        #retrieve the index list of colors for a already known instance color and add the new index with that color to it
        else:
            mesh_by_color_dict[result_integer].append(idx)
            mesh_color_uns[uns_result_integer].append(idx)
        
    keys_list = list(mesh_by_color_dict.keys())

    
    keys_list_uns = list(mesh_color_uns.keys())
    for tam in range(len(keys_list_uns)):
        l = keys_list_uns[tam].split('.')
        decimals = [f'0.{part[:2]}' for part in l[1:]]
        result = ' '.join(decimals)
        mesh_colors.append(result)
    n = 0
    for idx, key in enumerate(keys_list):
        if key != '000':
            model_name = 'mesh' + str(mesh_nro)
            mesh_nro += 1
            mesh_filtered = mesh.select_by_index(mesh_by_color_dict[key])
            mesh_filtered.compute_vertex_normals()
            if n == 0:
                R, plane_model, meshcenter = transform_mesh(mesh_filtered)
            mesh_filtered.rotate(R, center=meshcenter).translate((0,0,-plane_model[3]))
            if n  == 0:
                vertices = np.asarray(mesh_filtered.vertices)
                for vertice in vertices:
                    vertice[2] = 0
                    new_vertices.append(vertice)
                mesh_filtered.vertices = o3d.utility.Vector3dVector(new_vertices)
                n = 1
            # o3d.visualization.draw_geometries([mesh_filtered])
            base_folder, meshes_folder = create_gazebo_dir()
            mesh_uri = meshes_folder + model_name + '.obj'
            o3d.io.write_triangle_mesh(meshes_folder + model_name + '.obj', mesh_filtered)
            xml_infos_dict['model_name'].append(base_folder + '/' + model_name)
            xml_infos_dict['mesh_uri'].append(mesh_uri)
            xml_infos_dict['mesh_color'].append(mesh_colors[idx])
            create_single_xml(xml_infos_dict)


if __name__ == "__main__":
    mesh_and_sdf_creation()