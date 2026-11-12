from markdowntoblocks import markdown_to_blocks
from bloktobloktype import block_to_block_type, BlockType
from splitnodes import text_to_textnodes
from textnode import TextType
from textnode import text_node_to_html_node, TextNode
from htmlnode import HtmlNode, LeafNode, ParentNode

def get_html_subnodes(text: str) -> list[LeafNode]:
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]

def create_html_from_nodes(html_nodes: list[LeafNode]) -> str:
    return ''.join([html_node.to_html() for html_node in html_nodes])

def node_to_code_block(node: str) -> LeafNode:
    lines = node.split('\n')
    code = '\n'.join(lines[1:-1]) + '\n'
    return ParentNode('pre', [LeafNode('code', code)])

def node_to_heading(node: str) -> HtmlNode:
    level = node.count('#')
    subnodes = get_html_subnodes(node[level + 1:])
    return ParentNode(f'h{level}', subnodes)

def node_to_quote(node: str) -> HtmlNode:
    text = '\n'.join(line.lstrip('>').lstrip() for line in node.split('\n'))
    return ParentNode('blockquote', get_html_subnodes(text))

def node_to_unordered_list(node: str) -> ParentNode:
    text_list = node.split('\n')
    parsed_text = []
    for text in text_list:
        item = text[2:].lstrip()
        parsed_text.append(ParentNode('li', get_html_subnodes(item)))
    return ParentNode('ul', parsed_text)

def node_to_ordered_list(node: str) -> ParentNode:
    text_list = node.split('\n')
    parsed_text = []
    for text in text_list:
        item = text.split('.', 1)[1].lstrip() if '.' in text else text
        parsed_text.append(ParentNode('li', get_html_subnodes(item)))
    return ParentNode('ol', parsed_text)

def node_to_paragraph(node: str) -> LeafNode:
    return ParentNode('p', get_html_subnodes(node))
    
def markdown_to_html_node(markdown: str):
    markdown_blocks = markdown_to_blocks(markdown)
    html_blocks = []

    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.CODE:
                html_blocks.append(node_to_code_block(block))
            case BlockType.HEADING:
                html_blocks.append(node_to_heading(block))
            case BlockType.QUOTE:
                html_blocks.append(node_to_quote(block))
            case BlockType.UNORDERED_LIST:
                html_blocks.append(node_to_unordered_list(block))
            case BlockType.ORDERED_LIST:
                html_blocks.append(node_to_ordered_list(block))
            case BlockType.PARAGRAPH:
                html_blocks.append(node_to_paragraph(block))

    return ParentNode('div', html_blocks)
        

