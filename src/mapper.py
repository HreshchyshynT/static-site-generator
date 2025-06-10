from textnode import TextType, TextNode
from htmlnode import LeafNode
from constants import IMAGES_REGEX, LINK_REGEX
import re


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.IMAGE:
            return LeafNode(
                "img",
                "",
                (
                    {"src": text_node.url, "alt": text_node.text}
                    if text_node.url
                    else None
                ),
            )
        case TextType.LINK:
            return LeafNode(
                "a",
                text_node.text,
                {"href": text_node.url},
            )
        case _:
            raise ValueError("invalid text type")


def split_nodes_delimiter(
    old_nodes,
    delimiter,
    text_type,
):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        splitted = node.text.split(delimiter)
        if len(splitted) == 1:
            # not found delimiter
            raise ValueError(f"invalid delimiter: {delimiter}")
        if len(splitted) % 2 == 0:
            raise ValueError("delimiter isnt paired")

        for i, t in enumerate(splitted):
            # delimited part is at the beginning or at the end of the text
            if (i == 0 or i == len(splitted) - 1) and len(t) == 0:
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(t, TextType.TEXT))
            else:
                new_nodes.append(TextNode(t, text_type))

    return new_nodes


def extract_markdown_images(text):
    return re.findall(IMAGES_REGEX, text)


def extract_markdown_links(text):
    return re.findall(LINK_REGEX, text)
