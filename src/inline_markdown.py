from textnode import TextType, TextNode
from constants import IMAGES_REGEX, LINK_REGEX
import re


def text_to_text_nodes(text):
    node = TextNode(text, TextType.TEXT)
    all_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    all_nodes = split_nodes_delimiter(all_nodes, "_", TextType.ITALIC)
    all_nodes = split_nodes_delimiter(all_nodes, "`", TextType.CODE)
    all_nodes = split_nodes_image(all_nodes)
    all_nodes = split_nodes_link(all_nodes)
    return all_nodes


def split_nodes_delimiter(
    old_nodes,
    delimiter,
    text_type,
):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        splitted = node.text.split(delimiter)
        if len(splitted) == 1:
            new_nodes.append(node)
            continue
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


def split_nodes_image(old_nodes):
    new_nodes = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            new_nodes.append(n)
        else:
            images = extract_markdown_images(n.text)
            if len(images) == 0:
                new_nodes.append(n)
            else:
                prev_end = 0
                for alt, url in images:
                    image_md = f"![{alt}]({url})"
                    im_start = n.text.index(image_md)
                    im_end = im_start + len(image_md)
                    text = n.text[prev_end:im_start]
                    if len(text) > 0:
                        new_nodes.append(TextNode(text, TextType.TEXT))
                    new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                    prev_end = im_end
                if prev_end < len(n.text) - 1:
                    new_nodes.append(TextNode(n.text[prev_end:], TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            new_nodes.append(n)
        else:
            images = extract_markdown_links(n.text)
            if len(images) == 0:
                new_nodes.append(n)
            else:
                prev_end = 0
                for alt, url in images:
                    im_start = n.text.index(f"[{alt}]")
                    url_wrapped = f"({url})"
                    link_end = n.text.index(url_wrapped) + len(url_wrapped)
                    text = n.text[prev_end:im_start]
                    if len(text) > 0:
                        new_nodes.append(TextNode(text, TextType.TEXT))
                    new_nodes.append(TextNode(alt, TextType.LINK, url))
                    prev_end = link_end
                if prev_end < len(n.text) - 1:
                    new_nodes.append(
                        TextNode(
                            n.text[prev_end:],
                            TextType.TEXT,
                        )
                    )
    return new_nodes


def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line.split(" ", maxsplit=1)[1].strip()
    raise Exception("No header found in markdown")
