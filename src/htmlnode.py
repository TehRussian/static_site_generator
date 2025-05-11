import html

class HTMLNode():
    
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
        
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        props_list = []
        for key, value in self.props.items():
            if value is not None:
                props_list.append(f' {key}="{html.escape(str(value))}"')
        return "".join(props_list)
    
    def __repr__(self):
        return f"Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props}"
    
    
class LeafNode(HTMLNode):
    
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)
        self.value = value
        
    def to_html(self):
        if self.value == None:
            raise ValueError("Value missing")
        if self.tag == None:
            return self.value
        return f'''<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'''
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)
    
    def to_html(self):
        child_string = ""
        if self.tag == None:
            raise ValueError("Tag argument missing")
        if self.children == None:
            raise ValueError("Children argument missing")
        
        for child in self.children:
            if not isinstance(child, HTMLNode):
                raise TypeError("All children must be instances of HTMLNode")
            out_child = child.to_html()
            child_string += out_child
        return f'''<{self.tag}>{child_string}</{self.tag}>'''
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"