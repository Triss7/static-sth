import os
import shutil

def deploy_to_public(source, target):
    if os.path.exists(target):
        if not os.path.isdir(target):
            raise NotADirectoryError(f'Target is not a directory: {target}')

        print(f'# removing tree of directory {target}')
        shutil.rmtree(target)

    os.makedirs(target, exist_ok=True)

    print(f'# copy files and directories from {source}')
    for el in os.listdir(source):
        print(f'# managing the {el}')
        el_path = os.path.join(source, el)
        print(f'el path is: {el_path}')
        dst_path= os.path.join(target, el)
        print(f'dst path is: {dst_path}')
        print(f'# is {el} a file? {os.path.isfile(el_path)}')
        if os.path.isfile(el_path):
            print(f'Does file exists in source? {os.path.exists(el_path)}')
            print(f'Does file exists in target? {os.path.exists(dst_path)}')
            print(f'# copying {el} file')
            shutil.copy(el_path, dst_path)
        else:
            print(f'# copying the {el} directory')
            os.makedirs(dst_path, exist_ok=True)
            deploy_to_public(el_path, dst_path)

    print(f'done')


        
    
