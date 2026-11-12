import re

def extract_title(text: str) -> str:
    pattern = r"^#\s+(.+)$"
    match = re.search(pattern, text, re.MULTILINE)
    if not match:
        raise Exception('No title was spotted!')

    return match.group(1).lstrip("# \t").strip()
