import sys
import unittest
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SRC_DIR.parent
sys.path.insert(0, str(SRC_DIR))
sys.path.insert(0, str(PROJECT_DIR))

from markdowntoblocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_returns_one_block_for_text_without_blank_lines(self):
        markdown = "# Heading\nThis is the body."

        result = markdown_to_blocks(markdown)

        self.assertEqual(result, ["# Heading\nThis is the body."])

    def test_splits_markdown_on_blank_lines(self):
        markdown = "# Heading\n\nThis is a paragraph.\n\n- one\n- two"

        result = markdown_to_blocks(markdown)

        self.assertEqual(
            result,
            ["# Heading", "This is a paragraph.", "- one\n- two"],
        )

    def test_strips_whitespace_around_each_block(self):
        markdown = "  # Heading  \n\n  paragraph text  "

        result = markdown_to_blocks(markdown)

        self.assertEqual(result, ["# Heading", "paragraph text"])

    def test_ignores_empty_blocks_from_repeated_blank_lines(self):
        markdown = "# Heading\n\n\n\nParagraph"

        result = markdown_to_blocks(markdown)

        self.assertEqual(result, ["# Heading", "Paragraph"])

    def test_preserves_newlines_inside_a_block(self):
        markdown = "- first item\n- second item\n\n> quote"

        result = markdown_to_blocks(markdown)

        self.assertEqual(result, ["- first item\n- second item", "> quote"])

    def test_returns_empty_list_for_empty_markdown(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_returns_empty_list_for_whitespace_only_markdown(self):
        self.assertEqual(markdown_to_blocks(" \n\n  \n"), [])


if __name__ == "__main__":
    unittest.main()
