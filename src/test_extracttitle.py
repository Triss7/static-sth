import sys
import unittest
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SRC_DIR))

from extracttitle import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extracts_title_from_level_one_heading(self):
        self.assertEqual(extract_title("# My blog title\n\nContent"), "My blog title")

    def test_returns_first_level_one_heading(self):
        markdown = "Intro\n## Not the title\n# Actual title\n# Another title"

        self.assertEqual(extract_title(markdown), "Actual title")

    def test_strips_leading_hashes_and_whitespace_from_title(self):
        markdown = "#   ## Actual title   \n\nContent"

        self.assertEqual(extract_title(markdown), "Actual title")

    def test_ignores_headings_without_a_space_after_hash(self):
        markdown = "## Subtitle\n#Not a title\nParagraph"

        with self.assertRaisesRegex(Exception, "No title was spotted!"):
            extract_title(markdown)

    def test_raises_when_title_is_missing(self):
        with self.assertRaisesRegex(Exception, "No title was spotted!"):
            extract_title("Paragraph without a title")


if __name__ == "__main__":
    unittest.main()
