import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_different_url(self):
        node = TextNode("Text", TextType.LINK, "https://someurl.com")
        node2 = TextNode("Text", TextType.LINK, "https://anotherurl.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_different_text(self):
        node = TextNode("Text1", TextType.LINK, "https://someurl.com")
        node2 = TextNode("Text2", TextType.LINK, "https://someurl.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_different_type(self):
        node = TextNode("Text", TextType.BOLD)
        node2 = TextNode("Text", TextType.ITALIC)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
