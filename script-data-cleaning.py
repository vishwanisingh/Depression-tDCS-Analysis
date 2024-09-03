import os
import shutil

# main_folder = 'Depression-Sample-dataset-AIIMS/32electrodes/Sham/1Pre-BML'

for folder_name in os.listdir(main_folder):
    inner_folder_name = folder_name.split("_")[-1]
    new_folder_path =  os.path.join(main_folder, inner_folder_name)
    os.mkdir(new_folder_path)
    inner_folder_path = os.path.join(main_folder, folder_name)
    if len(os.listdir(inner_folder_path)) == 1:
        inner_folder_path = os.path.join(inner_folder_path, os.listdir(inner_folder_path)[0])
        
    for file_name in os.listdir(inner_folder_path):
        file_path = os.path.join(inner_folder_path, file_name)
        shutil.move(file_path, os.path.join(new_folder_path, file_name))