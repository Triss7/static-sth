from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = ('paragraph', None)
    HEADING = ('heading', r'^#{1,6} ')
    CODE = ('code', r"^```([a-zA-Z]*)\n(.*?)\n^```$")
    QUOTE = ('quote', r'^(>+)\s*(.*)')
    UNORDERED_LIST = ('unordered_list', r"^[\*\-\+]\s+")
    ORDERED_LIST = ('ordered_list', r"^\d+[\.\)]\s+")


def block_to_block_type(block) -> BlockType:
    for block_type in BlockType:
        _, regex = block_type.value
        if regex and re.match(regex, block, re.DOTALL | re.MULTILINE):
            return block_type

    return BlockType.PARAGRAPH

