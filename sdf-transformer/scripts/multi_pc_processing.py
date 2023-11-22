# examples/Python/Basic/pointcloud.py

import numpy as np
import open3d as o3d
from sdf_writer import create_xml
from move_files import create_gazebo_dir
import os
def mesh_and_sdf_creation():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    mesh_nro = 0
    mesh_by_color_dict = {}
    xml_infos_dict = {
        'model_name': [],
        'mesh_uri':[],
        'collision_scale':[]
    }
    mesh = o3d.io.read_triangle_mesh("/home/joao/tcc/final-version/sdf-generator/pc-files/results/mesh_instances.ply")
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
        if key != '000':
            model_name = 'mesh' + str(mesh_nro)
            mesh_nro += 1
            mesh_uri = dir_path + '/' + model_name + '.obj'
            mesh_filtered = mesh.select_by_index(mesh_by_color_dict[key])
            mesh_filtered.compute_vertex_normals()
            # o3d.visualization.draw_geometries([mesh_filtered])
            base_folder, meshes_folder = create_gazebo_dir()
            o3d.io.write_triangle_mesh(meshes_folder + model_name + '.obj', mesh_filtered)
            xml_infos_dict['model_name'].append(base_folder + '/' + model_name)
            xml_infos_dict['mesh_uri'].append(mesh_uri)



if __name__ == "__main__":
    mesh_and_sdf_creation()