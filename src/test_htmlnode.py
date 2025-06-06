import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )

    def test_eq(self):
        node1 = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node1, node2)

    def test_not_eq(self):
        node1 = HTMLNode(tag="a")
        node2 = HTMLNode(tag="p")
        self.assertNotEqual(node1, node2)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_raw_test_when_no_tag(self):
        node = LeafNode(None, "Hello world")
        self.assertEqual(node.to_html(), "Hello world")

    def test_leaf_to_html_p_and_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), expected)


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child</span></div>",
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_keeps_children_order(self):
        children = [
            LeafNode("b", "child1"),
            LeafNode(None, "child2"),
            LeafNode("a", "child3", {"href": "https://google.com"}),
        ]
        parent_node = ParentNode("div", children)
        self.assertEqual(
            parent_node.to_html(),
            '<div><b>child1</b>child2<a href="https://google.com">child3</a></div>',
        )

    def test_no_tag_raise_error(self):
        parent = ParentNode(None, [])
        with self.assertRaises(ValueError) as cm:
            parent.to_html()
        self.assertEqual(
            str(cm.exception),
            "all parent node must have a tag",
        )

    def test_no_children_raise_error(self):
        parent = ParentNode("div", None)
        with self.assertRaises(ValueError) as cm:
            parent.to_html()
        self.assertEqual(
            str(cm.exception),
            "all parent node must have children",
        )

    def test_empty_children(self):
        parent = ParentNode("div", [])
        self.assertEqual(parent.to_html(), "<div></div>")

    def test_props_includes(self):
        children = [
            LeafNode(None, "test"),
            ParentNode("div", [], props={"prop": "value"}),
        ]
        parent_node = ParentNode("div", children)
        self.assertEqual(
            parent_node.to_html(),
            '<div>test<div prop="value"></div></div>',
        )
