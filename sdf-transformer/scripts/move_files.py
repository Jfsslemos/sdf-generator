import os
import shutil
def create_folder(goal_dir: str, folder_to_create: str):
    folder = goal_dir + folder_to_create
    new_folder = folder
    i = 0
    j=1
    while i == 0:
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)
            i = 1
        else:
            new_folder = goal_dir + folder_to_create + f'_{j}'
            j += 1
    return new_folder

def create_gazebo_dir():
    base_gazebo_dir = '/home/joao/.gazebo/models/'
    created_folder = create_folder(base_gazebo_dir, 'obj')
    #print(created_folder)
    meshes_folder = create_folder(created_folder, '/meshes/')
    return created_folder, meshes_folder

def move_to_gazebo_folder():
    create_gazebo_dir()

if __name__ == "__main__":
    move_to_gazebo_folder()
    #copy_files('/home/joao/tcc/final-version/sdf-generator/sdf-transformer/models-sdf/box.sdf', '/home/joao/tcc/final-version/sdf-generator/sdf-transformer/models-stl')
    # goal_dir = '/home/joao/.gazebo/models/'
    # extesion_1 = '.sdf'
    # move_files_by_extesion(goal_dir, extesion_1)



    #create the folder in the gazebo directory
    # model_name_wo_ext = model_name.split('.')
    # model_dir = goal_dir + model_name_wo_ext[0]
    # create_folder(goal_dir, model_name_wo_ext[0])