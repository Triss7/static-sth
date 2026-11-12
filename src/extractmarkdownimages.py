import re

def extraxt_markdown_images(text):
    return re.findall(r"!\[([^\]]*)\]\(([^)]+)\)" , text)

def etraxt_markdown_links(text):
    return re.findall(r"\[([^\]]*)\]\(([^)]+)\)", text)

