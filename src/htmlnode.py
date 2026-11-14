class HtmlNode:
    def __init__(self, tag = '', value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError('Not implemented!')

    def props_to_html(self):
        if self.props is None:
            return ''

        result = ''
        for key, value in self.props.items():
            result = result + f' {key}="{value}"'

        return result

    def __repr__(self):
        return f'HtmlNode({self.tag}, {self.value}, {self.children}, {self.props})'


class LeafNode(HtmlNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError('All leafs has to have a value!')

        if self.tag is None:
            return f'{self.value}'

        props_to_html = self.props_to_html()
        return f'<{self.tag}{props_to_html}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f'HtmlNode({self.tag}, {self.value}, {self.props})'

class ParentNode(HtmlNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError('Tag cannot be None!')

        if self.children is None:
            raise ValueError('Children cannot be none!')

        props_to_html = self.props_to_html()
        return f'<{self.tag}{props_to_html}>{''.join([child.to_html() for child in self.children])}</{self.tag}>'

