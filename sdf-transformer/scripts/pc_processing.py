# examples/Python/Basic/pointcloud.py

import numpy as np
import open3d as o3d

dict_colors = {}
mesh_nro = 0
prev_color = None
idx_list = []
mesh_by_color_dict = {}
print("Testing mesh in Open3D...")
mesh = o3d.io.read_triangle_mesh("/home/joao/tcc/final-version/sdf-generator/pc-files/results/mesh_instances.ply")
# print(mesh)
# print('Vertices:')
# print(np.asarray(mesh.vertices))
# print('Triangles:')
# print(np.asarray(mesh.triangles))
# print("Computing normal and rendering it.")
mesh.compute_vertex_normals()
# print(np.asarray(mesh.triangle_normals))


vertex_colors = mesh.vertex_colors

for idx, color in enumerate(vertex_colors):

    #function to make the color hashable
    scaled_values = [int(value * 255) for value in np.asarray(color)]
    result_integer = str(''.join(map(str, scaled_values)))

    #function to set a mesh name for each instance color 
    if result_integer not in list(mesh_by_color_dict.keys()):
        mesh_by_color_dict[result_integer] = [idx]

    #retrieve the index list of colors for a already known instance color and add the new index with that color to it
    else:
        mesh_by_color_dict[result_integer].append(idx)
    
keys_list = list(mesh_by_color_dict.keys())

for key in keys_list:
    mesh_filtered = mesh.select_by_index(mesh_by_color_dict[key])
    o3d.visualization.draw_geometries([mesh_filtered])
