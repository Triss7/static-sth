import os
from pathlib import Path
from generatepage import generate_page

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for el in os.listdir(dir_path_content):
        print(f'# Checking {el} element')
        el_path = os.path.join(dir_path_content, el)
        dest_path = os.path.join(dest_dir_path, el)
        print(f'# Is {el_path} a file?')
        if os.path.isfile(el_path):
            html_path = Path(dest_path).with_suffix('.html')
            print(f'# Generating page for {el_path} and copying file to {html_path}')
            generate_page(el_path, template_path, html_path, basepath)
        else:
            print(f'{el_path} is directory, need to go recursive')
            generate_pages_recursive(el_path, template_path, dest_path, basepath)
        
        

