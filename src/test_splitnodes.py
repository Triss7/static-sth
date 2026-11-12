import sys
import unittest
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SRC_DIR))

from splitnodes import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_splits_text_node_into_plain_and_formatted_nodes(self):
        nodes = [TextNode("This is **bold** text", TextType.TEXT)]

        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)

        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_splits_multiple_formatted_sections(self):
        nodes = [TextNode("**one** and **two**", TextType.TEXT)]

        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)

        self.assertEqual(
            result,
            [
                TextNode("one", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.BOLD),
            ],
        )

    def test_preserves_text_node_without_delimiters(self):
        node = TextNode("plain text", TextType.TEXT)

        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(result, [node])

    def test_preserves_non_text_nodes(self):
        node = TextNode("https://example.com", TextType.LINK)

        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(result, [node])

    def test_raises_for_unmatched_delimiter(self):
        nodes = [TextNode("This is **bold", TextType.TEXT)]

        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes, "**", TextType.BOLD)


if __name__ == "__main__":
    unittest.main()
