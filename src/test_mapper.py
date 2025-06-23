import unittest
from mapper import (
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_link,
    split_nodes_image,
    text_to_nodes,
    markdown_to_blocks,
    markdown_to_html_node,
)
from textnode import TextNode, TextType
from test_data import (
    BASIC_MARKDOWN,
    CODE_MARKDOWN,
    IMAGES_LINKS,
    QUOTE_BLOCK,
)


class TestNodeToHtml(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_image(self):
        node = TextNode(
            "This is an image", TextType.IMAGE, "https://example.com/image.png"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {
                "src": "https://example.com/image.png",
                "alt": "This is an image",
            },
        )

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_invalid_text_type(self):
        node = TextNode("This is an invalid type", "invalid_type")
        with self.assertRaises(ValueError) as cm:
            text_node_to_html_node(node)
        self.assertEqual(
            str(cm.exception),
            "invalid text type",
        )


class TestSplitNodeDelimeter(unittest.TestCase):

    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_code_delimiter_not_found(self):
        node = TextNode("This is text without a code block", TextType.TEXT)
        new_nodes = split_nodes_delimiter(
            [node],
            "_",
            TextType.ITALIC,
        )
        self.assertListEqual(
            [node],
            [node],
        )

    def test_code_delimiter_not_paired(self):
        node = TextNode("This is text with a `code block", TextType.TEXT)
        with self.assertRaises(ValueError) as cm:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            str(cm.exception),
            "delimiter isnt paired",
        )

    def test_code_delimiter_empty_text(self):
        node = TextNode("This is text with a `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
            ],
        )

    def test_italic_delimeter(self):
        node = TextNode("some text _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("some text ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
        )

    def test_extracts_markdown_images(self):
        text = "This is a text with an ![image](https://example.com/image.png) in it."
        images = extract_markdown_images(text)
        self.assertListEqual(
            images,
            [
                (
                    "image",
                    "https://example.com/image.png",
                )
            ],
        )

    def test_extracts_links(self):
        text = "This is a text with a [link](https://example.com) in it."
        links = extract_markdown_links(text)
        self.assertListEqual(
            links,
            [
                (
                    "link",
                    "https://example.com",
                )
            ],
        )

    def test_extracts_multiple_images(self):
        text = (
            "This is a text with an ![image1](https://example.com/image1.png) "
            "and ![image2](https://example.com/image2.png) in it."
        )
        images = extract_markdown_images(text)
        self.assertListEqual(
            images,
            [
                ("image1", "https://example.com/image1.png"),
                ("image2", "https://example.com/image2.png"),
            ],
        )

    def test_extracts_multiple_links(self):
        text = (
            "This is a text with a [link1](https://example.com/link1) "
            "and [link2](https://example.com/link2) in it."
        )
        links = extract_markdown_links(text)
        self.assertListEqual(
            links,
            [
                ("link1", "https://example.com/link1"),
                ("link2", "https://example.com/link2"),
            ],
        )


class TestSplitNodes(unittest.TestCase):

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and [link](https://link.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(
                    "This is text with an ",
                    TextType.TEXT,
                ),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://i.imgur.com/zjjcJKZ.png",
                ),
                TextNode(
                    " and another ",
                    TextType.TEXT,
                ),
                TextNode(
                    "second image",
                    TextType.IMAGE,
                    "https://i.imgur.com/3elNhQu.png",
                ),
                TextNode(" and [link](https://link.com)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://example.com) and another [second link](https://example.com/second)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link",
                    TextType.LINK,
                    "https://example.com/second",
                ),
            ],
            new_nodes,
        )

    def test_split_links_no_links(self):
        node = TextNode("This is text without links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("This is text without links", TextType.TEXT)],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode("This is text without images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This is text without images", TextType.TEXT)],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://www.example.COM/IMAGE.PNG",
                ),
            ],
            new_nodes,
        )


class TestTextToNodes(unittest.TestCase):
    def test_text_to_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_nodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image",
                    TextType.IMAGE,
                    "https://i.imgur.com/fJRm4Vk.jpeg",
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestMarkdownToHtml(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_basic_markdown(self):
        node = markdown_to_html_node(BASIC_MARKDOWN)
        html = node.to_html()

    def test_quote_block(self):
        node = markdown_to_html_node(QUOTE_BLOCK)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote><p>Dorothy followed her through many of the beautiful rooms in her castle.</p><p>The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.</p></blockquote></div>",
            msg=f"html:\n{repr(html)}\ninput:\n{repr(QUOTE_BLOCK)}",
        )
