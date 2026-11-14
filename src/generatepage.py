import os
from markdowntohtmlnode import markdown_to_html_node
from extracttitle import extract_title

def generate_page(from_path, template_path, dest_path, basepath):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')

    with open(from_path, 'r') as content_file:
        content_data = content_file.read()
        print(f'Content data available')

        with open(template_path, 'r') as template_file:
            template_data = template_file.read()
            print(f'template data available')

            print(f'Changing content to html nodes')
            html_node = markdown_to_html_node(content_data)

            print(f'Changing html nodes to html file')
            html_text = html_node.to_html()

            print(f'Extraxcing title')
            title = extract_title(content_data)
            
            print(f'Replacing the Title with {title}')
            template_data = template_data.replace('{{ Title }}', title)

            print(f'Replacing the content with html text')
            template_data = template_data.replace('{{ Content }}', html_text)

            print(f'Replacing src="/ with src="{basepath}')
            template_data = template_data.replace('src="/', f'src="{basepath}')

            print(f'Replacing href="/ with href="{basepath}')
            template_data = template_data.replace('href="/', f'href="{basepath}')

            print(f'Getting the dirname of {dest_path}')
            dirname = os.path.dirname(dest_path)

            print(f'Creating directories for {dirname}')
            os.makedirs(dirname, exist_ok=True)

            print('Writting a file')
            with open(dest_path, 'w') as dest_file:
                dest_file.write(template_data)
