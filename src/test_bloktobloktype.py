import sys
import unittest
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SRC_DIR.parent
sys.path.insert(0, str(SRC_DIR))
sys.path.insert(0, str(PROJECT_DIR))

from bloktobloktype import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    def test_identifies_headings(self):
        for level in range(1, 7):
            with self.subTest(level=level):
                self.assertEqual(
                    block_to_block_type(f"{'#' * level} Heading"),
                    BlockType.HEADING,
                )

    def test_does_not_identify_invalid_headings(self):
        for block in ("####### Heading", "#Heading", "#"):
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_identifies_code_blocks(self):
        block = "```python\nprint('hello')\n```"

        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_identifies_quote_blocks(self):
        self.assertEqual(
            block_to_block_type("> A quoted line"),
            BlockType.QUOTE,
        )

    def test_identifies_unordered_lists(self):
        for marker in ("-", "*", "+"):
            with self.subTest(marker=marker):
                self.assertEqual(
                    block_to_block_type(f"{marker} List item"),
                    BlockType.UNORDERED_LIST,
                )

    def test_identifies_ordered_lists(self):
        for marker in ("1.", "2)", "10."):
            with self.subTest(marker=marker):
                self.assertEqual(
                    block_to_block_type(f"{marker} List item"),
                    BlockType.ORDERED_LIST,
                )

    def test_defaults_to_paragraph(self):
        self.assertEqual(
            block_to_block_type("A regular paragraph."),
            BlockType.PARAGRAPH,
        )


if __name__ == "__main__":
    unittest.main()
