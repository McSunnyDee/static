from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Missing Tag")
        if not self.children:
            raise ValueError("Missing Children")
    
        return self.recursive(self.children)
    
    def recursive(self, children):
        string_of_children = ""
        for child in children:
            if not child.children:
                string_of_children += f'<{child.tag}{child.props_to_html()}>{child.value}</{child.tag}>'
            else:
                string_of_children += f'{child.recursive(child.children)}'
        return f'<{self.tag}{self.props_to_html()}>{string_of_children}</{self.tag}>'