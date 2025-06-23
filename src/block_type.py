from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


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
        return BlockType.UNORDERED_LIST

    if all(
        [line.startswith(f"{i + 1}. ") for i, line in enumerate(lines)],
    ):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
