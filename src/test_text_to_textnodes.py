import sys
import unittest
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SRC_DIR.parent
sys.path.insert(0, str(SRC_DIR))
sys.path.insert(0, str(PROJECT_DIR))

from splitnodes import text_to_textnodes
from textnode import TextNode, TextType


class TestTextToTextNodes(unittest.TestCase):
    def test_converts_plain_text(self):
        result = text_to_textnodes("plain text")

        self.assertEqual(result, [TextNode("plain text", TextType.TEXT)])

    def test_converts_bold_text(self):
        result = text_to_textnodes("This is **bold** text")

        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_converts_italic_text(self):
        result = text_to_textnodes("This is _italic_ text")

        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_converts_code_text(self):
        result = text_to_textnodes("Use `print()` here")

        self.assertEqual(
            result,
            [
                TextNode("Use ", TextType.TEXT),
                TextNode("print()", TextType.CODE),
                TextNode(" here", TextType.TEXT),
            ],
        )

    def test_converts_image(self):
        result = text_to_textnodes("A ![logo](logo.svg) image")

        self.assertEqual(
            result,
            [
                TextNode("A ", TextType.TEXT),
                TextNode("logo", TextType.IMAGE, "logo.svg"),
                TextNode(" image", TextType.TEXT),
            ],
        )

    def test_converts_link(self):
        result = text_to_textnodes("Visit [Boot.dev](https://boot.dev)")

        self.assertEqual(
            result,
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode("Boot.dev", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_converts_mixed_markdown(self):
        result = text_to_textnodes(
            "A **bold** and _italic_ `code` with [link](url) and ![image](img.png)."
        )

        self.assertEqual(
            result,
            [
                TextNode("A ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
                TextNode(" and ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "img.png"),
                TextNode(".", TextType.TEXT),
            ],
        )


if __name__ == "__main__":
    unittest.main()
