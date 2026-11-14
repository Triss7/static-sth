import unittest
from htmlnode import HtmlNode, LeafNode, ParentNode

class TestHtmlNode(unittest.TestCase):
    def test_value_none(self):
        children = [
                HtmlNode('input', 'test', None, {type: 'text'}),
                HtmlNode('button', 'test2', None)
                ]
        html1 = HtmlNode('div', None, children)

        self.assertIsNone(html1.value)

    def test_children_none(self):
        children = [
            HtmlNode('input', 'test', None, {type: 'text'}),
            HtmlNode('button', 'test2', None)
        ]

        html1 = HtmlNode('input', 'someValue', children)

        self.assertEqual(html1.value, 'someValue')
        self.assertIsNotNone(html1.children)

    def test_props_to_html(self):
        props = {
                "href": "www.example.com",
                "target": "_blank"
                }

        html1 = HtmlNode('a', None, None, props)
        prop_in_line = html1.props_to_html()

        self.assertEqual(prop_in_line, ' href="www.example.com" target="_blank"')


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node  = LeafNode("a", "Test link", { "href": "www.example.com", "target": "_blank" })
        self.assertEqual(node.to_html(), '<a href="www.example.com" target="_blank">Test link</a>')

class TestParentNode(unittest.TestCase):
    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", [])

        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_with_multiple_props(self):
        parent_node = ParentNode(
            "div",
            [],
            {"class": "container", "id": "main"},
        )

        self.assertEqual(
            parent_node.to_html(),
            '<div class="container" id="main"></div>',
        )

    def test_to_html_with_mixed_child_nodes(self):
        child_node = ParentNode("p", [LeafNode("b", "bold"), LeafNode("i", "italic")])
        parent_node = ParentNode("div", [child_node])

        self.assertEqual(
            parent_node.to_html(),
            "<div><p><b>bold</b><i>italic</i></p></div>",
        )

    def test_to_html_raises_when_tag_is_none(self):
        parent_node = ParentNode(None, [])

        with self.assertRaisesRegex(ValueError, "Tag cannot be None!"):
            parent_node.to_html()

    def test_to_html_raises_when_children_are_none(self):
        parent_node = ParentNode("div", None)

        with self.assertRaisesRegex(ValueError, "Children cannot be none!"):
            parent_node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_children_and_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "w-100"})
        self.assertEqual(parent_node.to_html(), '<div class="w-100"><span>child</span></div>')

    def test_to_html_with_two_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2= LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2])

        self.assertEqual(
                parent_node.to_html(),
                "<div><span>child1</span><span>child2</span></div>"
                )

if __name__ == "__main__":
    unittest.main()
