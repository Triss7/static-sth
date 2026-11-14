import sys
import unittest
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SRC_DIR))

from extractmarkdown import (
    etraxt_markdown_links,
    extraxt_markdown_images,
)


class TestExtractMarkdown(unittest.TestCase):
    def test_extracts_one_markdown_image(self):
        text = "A logo: ![Boot.dev logo](https://boot.dev/logo.png)"

        result = extraxt_markdown_images(text)

        self.assertEqual(
            result,
            [("Boot.dev logo", "https://boot.dev/logo.png")],
        )

    def test_extracts_multiple_markdown_images(self):
        text = "![one](one.png) and ![two](two.png)"

        result = extraxt_markdown_images(text)

        self.assertEqual(result, [("one", "one.png"), ("two", "two.png")])

    def test_extracts_one_markdown_link(self):
        text = "Visit [Boot.dev](https://boot.dev) for tutorials."

        result = etraxt_markdown_links(text)

        self.assertEqual(result, [("Boot.dev", "https://boot.dev")])

    def test_extracts_multiple_markdown_links(self):
        text = "[one](one.com) and [two](two.com)"

        result = etraxt_markdown_links(text)

        self.assertEqual(result, [("one", "one.com"), ("two", "two.com")])

    def test_returns_empty_list_when_no_matches_exist(self):
        text = "This text contains no markdown links or images."

        self.assertEqual(extraxt_markdown_images(text), [])
        self.assertEqual(etraxt_markdown_links(text), [])


if __name__ == "__main__":
    unittest.main()
