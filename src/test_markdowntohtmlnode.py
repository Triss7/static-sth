import sys
import unittest
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SRC_DIR.parent
sys.path.insert(0, str(SRC_DIR))
sys.path.insert(0, str(PROJECT_DIR))

from markdowntohtmlnode import markdown_to_html_node


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_returns_empty_div_for_empty_markdown(self):
        self.assertEqual(markdown_to_html_node("").to_html(), "<div></div>")

    def test_converts_paragraph(self):
        markdown = "This is a paragraph."

        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            "<div><p>This is a paragraph.</p></div>",
        )

    def test_converts_inline_markdown_in_paragraph(self):
        markdown = "This is **bold**, _italic_, and `code`."

        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            "<div><p>This is <b>bold</b>, <i>italic</i>, and <code>code</code>.</p></div>",
        )

    def test_converts_heading(self):
        self.assertEqual(
            markdown_to_html_node("### A heading").to_html(),
            "<div><h3>A heading</h3></div>",
        )

    def test_converts_code_block(self):
        markdown = "```python\nprint('hello')\n```"

        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            "<div><pre><code>print('hello')\n</code></pre></div>",
        )

    def test_converts_quote(self):
        self.assertEqual(
            markdown_to_html_node("> A quote").to_html(),
            "<div><blockquote>A quote</blockquote></div>",
        )

    def test_converts_unordered_list(self):
        markdown = "- first\n- second"

        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            "<div><ul><li>first</li><li>second</li></ul></div>",
        )

    def test_converts_ordered_list(self):
        markdown = "1. first\n2. second"

        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            "<div><ol><li>first</li><li>second</li></ol></div>",
        )

    def test_converts_multiple_blocks(self):
        markdown = "# Title\n\nA paragraph.\n\n- one\n- two"

        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            "<div><h1>Title</h1><p>A paragraph.</p>"
            "<ul><li>one</li><li>two</li></ul></div>",
        )


if __name__ == "__main__":
    unittest.main()
