from enum import Enum
from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_text_nodes
from textnode import text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def block_to_block_type(block):
    block_start = block.split(" ")[0]
    headings = {
        "#",
        "##",
        "###",
        "####",
        "#####",
        "######",
    }

    if block_start in headings:
        return BlockType.HEADING

    lines = block.split("\n")

    if lines[0].strip().startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    if block_start.startswith(">") and all(
        [line.startswith(">") for line in lines],
    ):
        return BlockType.QUOTE

    if all(
        [line.startswith("- ") for line in lines],
    ):
        return BlockType.ULIST

    if all(
        [line.startswith(f"{i + 1}. ") for i, line in enumerate(lines)],
    ):
        return BlockType.OLIST

    return BlockType.PARAGRAPH


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
            case BlockType.ULIST:
                node.children = get_list_items(b)
            case BlockType.OLIST:
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
    text = " ".join(
        [
            line.split(" ", maxsplit=1)[1]
            for line in block.splitlines()
            if len(line.strip()) > 1
        ]
    )

    return text_to_html_nodes(text)


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
        case BlockType.ULIST:
            return "ul"
        case BlockType.OLIST:
            return "ol"
        case _:
            raise ValueError(f"invalid block type: {bt}")


def text_to_html_nodes(text):
    text_nodes = text_to_text_nodes(text)
    children = [text_node_to_html_node(n) for n in text_nodes]
    return children
