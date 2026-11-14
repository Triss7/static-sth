from textnode import TextNode, TextType
from pathlib import Path
from deploytopublic import deploy_to_public
from generatepagesrecursive import generate_pages_recursive

def main():
    text_node = TextNode('This is some anchor text', TextType.LINK,' https://www.boot.dev')

    print(repr(text_node))
    src_dir = Path(__file__).resolve().parent
    root_dir = src_dir.parent
    static_path = root_dir / 'static'
    public_path = root_dir / 'public'
    deploy_to_public(static_path, public_path)
    content_path = root_dir / 'content/'
    template_path = root_dir / 'template.html'
    generate_pages_recursive(content_path, template_path, public_path)


main()

