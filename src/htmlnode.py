class HTMLNode:
    def __init__(
        self,
        tag=None,
        value=None,
        children=None,
        props=None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return ""

        html_values = []
        for key, value in self.props.items():
            html_values.append(f'{key}="{value}"')
        return " " + " ".join(html_values)

    def __eq__(self, other):
        if type(other) is not HTMLNode:
            return False

        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    def __repr__(self):
        return (
            f"HTMLNode({self.tag}, {self.value}, " + f"{self.children}, {self.props})"
        )


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf node must have a value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("all parent node must have a tag")
        if self.children is None:
            raise ValueError("all parent node must have children")
        html = [f"<{self.tag}{self.props_to_html()}>"]
        for child in self.children:
            html.append(child.to_html())
        html.append(f"</{self.tag}>")
        return "".join(html)
