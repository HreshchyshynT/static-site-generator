import unittest
from block_type import BlockType, block_to_block_type


class TestBlockType(unittest.TestCase):
    def test_paragraph(self):
        text = """
some paragraph
without any special characters"""
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type(text),
        )

    def test_heading(self):
        block = "## heading 2"
        self.assertEqual(
            BlockType.HEADING,
            block_to_block_type(block),
        )

    def test_code(self):
        block = """```
def foo():
    return "bar"
```"""
        self.assertEqual(
            BlockType.CODE,
            block_to_block_type(block),
        )

    def test_quotes(self):
        block = """> first quote
> second quote"""
        self.assertEqual(
            BlockType.QUOTE,
            block_to_block_type(block),
        )

    def test_unordered_list(self):
        block = """- something
- something else"""
        self.assertEqual(
            BlockType.UNORDERED_LIST,
            block_to_block_type(block),
        )

    def test_ordered_list_matches(self):
        block = """1. First
2. Second
3. Third"""
        self.assertEqual(
            BlockType.ORDERED_LIST,
            block_to_block_type(block),
        )

    def test_wrong_ordered_list(self):
        block = """2. First
2. Second
4. Third"""
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type(block),
        )
