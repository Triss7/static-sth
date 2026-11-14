import sys
import unittest
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SRC_DIR.parent
sys.path.insert(0, str(SRC_DIR))
sys.path.insert(0, str(PROJECT_DIR))

from splitnodes import (
    split_nodes_image,
    split_nodes_image_or_link,
    split_nodes_link,
)
from textnode import TextNode, TextType


class TestSplitNodesImage(unittest.TestCase):
    def test_splits_image_between_text_nodes(self):
        nodes = [TextNode("Before ![cat](cat.png) after", TextType.TEXT)]

        result = split_nodes_image(nodes)

        self.assertEqual(
            result,
            [
                TextNode("Before ", TextType.TEXT),
                TextNode("cat", TextType.IMAGE, "cat.png"),
                TextNode(" after", TextType.TEXT),
            ],
        )

    def test_splits_multiple_images_in_one_text_node(self):
        nodes = [TextNode("![one](one.png) and ![two](two.jpg)", TextType.TEXT)]

        result = split_nodes_image(nodes)

        self.assertEqual(
            result,
            [
                TextNode("one", TextType.IMAGE, "one.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.IMAGE, "two.jpg"),
            ],
        )

    def test_splits_image_when_it_is_the_entire_node(self):
        node = TextNode("![logo](logo.svg)", TextType.TEXT)

        result = split_nodes_image([node])

        self.assertEqual(result, [TextNode("logo", TextType.IMAGE, "logo.svg")])

    def test_preserves_text_node_without_images(self):
        node = TextNode("plain text", TextType.TEXT)

        result = split_nodes_image([node])

        self.assertEqual(result, [node])

    def test_preserves_non_text_nodes(self):
        node = TextNode("already linked", TextType.LINK, "https://example.com")

        result = split_nodes_image([node])

        self.assertEqual(result, [node])

    def test_raises_for_unmatched_image_delimiters(self):
        nodes = [TextNode("An image: ![cat](cat.png", TextType.TEXT)]

        with self.assertRaises(Exception):
            split_nodes_image(nodes)


class TestSplitNodesLink(unittest.TestCase):
    def test_splits_link_between_text_nodes(self):
        nodes = [TextNode("Visit [Boot.dev](https://boot.dev) today", TextType.TEXT)]

        result = split_nodes_link(nodes)

        self.assertEqual(
            result,
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode("Boot.dev", TextType.LINK, "https://boot.dev"),
                TextNode(" today", TextType.TEXT),
            ],
        )

    def test_splits_multiple_links_in_one_text_node(self):
        nodes = [TextNode("[one](one.test) and [two](two.test)", TextType.TEXT)]

        result = split_nodes_link(nodes)

        self.assertEqual(
            result,
            [
                TextNode("one", TextType.LINK, "one.test"),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.LINK, "two.test"),
            ],
        )

    def test_preserves_non_text_nodes(self):
        node = TextNode("![logo](logo.svg)", TextType.IMAGE, "logo.svg")

        result = split_nodes_link([node])

        self.assertEqual(result, [node])

    def test_raises_for_unmatched_link_delimiters(self):
        nodes = [TextNode("Visit [Boot.dev](https://boot.dev", TextType.TEXT)]

        with self.assertRaises(Exception):
            split_nodes_link(nodes)


class TestSplitNodesImageOrLink(unittest.TestCase):
    def test_shared_helper_uses_requested_text_type(self):
        image_nodes = [TextNode("![logo](logo.svg)", TextType.TEXT)]
        link_nodes = [TextNode("[Boot.dev](https://boot.dev)", TextType.TEXT)]

        self.assertEqual(
            split_nodes_image_or_link(image_nodes, TextType.IMAGE),
            [TextNode("logo", TextType.IMAGE, "logo.svg")],
        )
        self.assertEqual(
            split_nodes_image_or_link(link_nodes, TextType.LINK),
            [TextNode("Boot.dev", TextType.LINK, "https://boot.dev")],
        )


if __name__ == "__main__":
    unittest.main()
