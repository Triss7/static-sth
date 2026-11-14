import unittest
from htmlnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_text_node_to_html_node_text(self):
        node = text_node_to_html_node(TextNode("plain text", TextType.TEXT))

        self.assertIsInstance(node, LeafNode)
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, "plain text")

    def test_text_node_to_html_node_inline_styles(self):
        test_cases = [
            (TextType.BOLD, "b"),
            (TextType.ITALIC, "i"),
            (TextType.CODE, "code"),
        ]

        for text_type, tag in test_cases:
            with self.subTest(text_type=text_type):
                node = text_node_to_html_node(TextNode("styled text", text_type))
                self.assertEqual(node.tag, tag)
                self.assertEqual(node.value, "styled text")

    def test_text_node_to_html_node_link(self):
        node = text_node_to_html_node(
            TextNode("Boot.dev", TextType.LINK, "https://boot.dev")
        )

        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Boot.dev")
        self.assertEqual(node.props, {"href": "https://boot.dev"})

    def test_text_node_to_html_node_image(self):
        node = text_node_to_html_node(
            TextNode("Boot.dev logo", TextType.IMAGE, "logo.png")
        )

        self.assertEqual(node.tag, "img")
        self.assertEqual(node.value, "")
        self.assertEqual(node.props, {"src": "logo.png", "alt": "Boot.dev logo"})
        self.assertEqual(
            node.to_html(),
            '<img src="logo.png" alt="Boot.dev logo"></img>',
        )

    def test_text_node_to_html_node_rejects_unknown_type(self):
        node = TextNode("invalid", "invalid")

        with self.assertRaises(Exception):
            text_node_to_html_node(node)

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_diff_text(self):
        node = TextNode('Test 1', TextType.BOLD)
        node2 = TextNode('Test 2', TextType.BOLD)

        self.assertNotEqual(node,node2)

    def test_url_default(self):
        node = TextNode('Test 1', TextType.BOLD, None)
        node2 = TextNode('Test 1', TextType.BOLD)

        self.assertEqual(node, node2)

    def test_diff_type(self):
        node = TextNode('Test 1', TextType.TEXT)
        node2 = TextNode('Test 1', TextType.BOLD)

        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
