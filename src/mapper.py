from textnode import TextType, TextNode
from htmlnode import LeafNode, ParentNode
from constants import IMAGES_REGEX, LINK_REGEX
from block_type import block_to_block_type, BlockType

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
    return new_nodes


def text_to_nodes(text):
    node = TextNode(text, TextType.TEXT)
    all_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    all_nodes = split_nodes_delimiter(all_nodes, "_", TextType.ITALIC)
    all_nodes = split_nodes_delimiter(all_nodes, "`", TextType.CODE)
    all_nodes = split_nodes_image(all_nodes)
    all_nodes = split_nodes_link(all_nodes)
    return all_nodes


def markdown_to_blocks(markdown):
    # TODO: handle empty lines in code block
    # ```
    # some code
    #
    # ```
    # should treat as single code block
    blocks = list(
        filter(
            lambda s: len(s) > 0,
            map(
                lambda s: s.strip(),
                markdown.split("\n\n"),
            ),
        )
    )
    return blocks


def markdown_to_html_node(markdown):
    root = ParentNode("div", [])
    blocks = markdown_to_blocks(markdown)

    for b in blocks:
        bt = block_to_block_type(b)
        node = ParentNode(block_type_to_tag(bt, b), [])
        match bt:
            case BlockType.PARAGRAPH:
                node = get_paragraph_node(b)
            case BlockType.HEADING:
                text = b.split(" ", maxsplit=1)[1]
                node = LeafNode(node.tag, text)
            case BlockType.CODE:
                node.children.append(get_code_block_node(b))

            case BlockType.QUOTE:
                node.children = get_quote_block_children(b)
            case BlockType.UNORDERED_LIST:
                node.children = get_list_items(b)
            case BlockType.ORDERED_LIST:
                node.children = get_list_items(b)
            case _:
                raise ValueError(f"invalid block type: {bt}")
        root.children.append(node)

    return root


def get_list_items(block):
    all_nodes = []
    lines = [line.split(" ", maxsplit=1)[1] for line in block.splitlines()]
    for line in lines:
        all_nodes.append(ParentNode("li", text_to_html_nodes(line)))
    return all_nodes


def get_code_block_node(b):
    code = b.split("```")
    # code block should end with \n
    node = LeafNode(
        "code",
        "\n".join([s for s in code[1].splitlines() if s.strip()]) + "\n",
    )
    return node


def get_quote_block_children(block):
    all_nodes = []
    lines = [line for line in block.splitlines() if len(line.strip()) > 1]
    for line in lines:
        content = line.split(">", maxsplit=1)[1].strip()
        node = get_paragraph_node(content)
        all_nodes.append(node)

    return all_nodes


def get_paragraph_node(content):
    content = " ".join(
        [line.strip() for line in content.splitlines() if line.strip()],
    )
    return ParentNode("p", text_to_html_nodes(content))


def block_type_to_tag(bt, block):
    match bt:
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.HEADING:
            n = len(block.split(" ")[0])
            return f"h{n}"
        case BlockType.CODE:
            return "pre"  # TODO: multiline code use pre and code tags
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.UNORDERED_LIST:
            return "ul"
        case BlockType.ORDERED_LIST:
            return "ol"
        case _:
            raise ValueError(f"invalid block type: {bt}")


def text_to_html_nodes(text):
    text_nodes = text_to_nodes(text)
    children = [text_node_to_html_node(n) for n in text_nodes]
    return children
