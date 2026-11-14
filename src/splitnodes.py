from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if node.text.count(delimiter) % 2 != 0:
            raise Exception('Markdown syntax in invalid! The {delimiter} missing closing tag!')

        for index, section in enumerate(node.text.split(delimiter)):
             if not section:
                continue

             node_type = TextType.TEXT if index % 2 == 0 else text_type
             new_nodes.append(TextNode(section, node_type))

    return new_nodes

def split_nodes_image_or_link(old_nodes: list[TextNode], text_type) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if node.text.count('(') != node.text.count(')') or node.text.count('[') != node.text.count(']'):
            raise Exception('Markdown syntax is invalid! The added image missing closing/opening sign')

        new_texts = []
        regex_whole = r"(!\[.*?\]\(.*?\))" if text_type == TextType.IMAGE else r"(\[.*?\]\(.*?\))"
        new_texts.extend(re.split(regex_whole, node.text))

        for text in new_texts:
            if not text:
                continue
            
            is_link = text_type == TextType.LINK and text[0] == '['
            is_image = text_type == TextType.IMAGE and text[0:2] == '!['
            if is_link or is_image:
                match_description = re.search(r'\[(.*?)\]', text)
                regex_url = r'!\[.*?\]\((.*?)\)' if text_type == TextType.IMAGE else r'\[.*?\]\((.*?)\)'
                match_url = re.search(regex_url, text)

                description = match_description.group(1) if match_description else ''
                url = match_url.group(1) if match_url else ''
                new_nodes.append(TextNode(description, text_type, url))

            else:
                new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_image_or_link(old_nodes, TextType.IMAGE)

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_image_or_link(old_nodes, TextType.LINK)

def text_to_textnodes(text):
    result = []
    node = TextNode(text, TextType.TEXT)
    # check for images
    result = split_nodes_image([node])

    # check for links
    result = split_nodes_link(result)

    # check the rest delimiters
    for delimiter, text_type in [('`', TextType.CODE), ('**', TextType.BOLD), ('_', TextType.ITALIC)]:
        result = split_nodes_delimiter(result, delimiter, text_type)

    return result
