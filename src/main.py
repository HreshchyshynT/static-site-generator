from textnode import TextNode, TextType
from mapper import markdown_to_html_node
import test_data


def main():
    node = markdown_to_html_node(test_data.CODE_MARKDOWN)
    print(node.to_html())


if __name__ == "__main__":
    main()
