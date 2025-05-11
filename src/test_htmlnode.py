import unittest

from htmlnode import *


class TestHtmlNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(props={"href": "https://example.com", "target": "_blank"})
        node2 = ' href="https://example.com" target="_blank"'
        self.assertEqual(node.props_to_html(), node2)
    def test_Raise_err(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()
    def test_Children_None(self):
        node = HTMLNode()
        node2 = []
        self.assertEqual(node.children, node2)
    def test_Props_Default(self):
        node = HTMLNode()
        self.assertEqual(node.props, {})
        
class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!")
        self.assertEqual(node.to_html(), "<a>Hello, world!</a>")
    def test_leaf_to_html_h(self):
        node = LeafNode("h", "Hello, world!")
        self.assertEqual(node.to_html(), "<h>Hello, world!</h>")
    def test_leaf_to_html_ahref(self):
        node = LeafNode("a", "Hello, world!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Hello, world!</a>')
    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")
        
class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_without_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")
    
    def test_to_html_nested_ParentNodes(self):
        nested = ParentNode(
            "div", 
            [
                ParentNode("span", [LeafNode(None, "Hello")]),
                LeafNode("p", "World!"),
            ],
        )
        self.assertEqual(nested.to_html(), "<div><span>Hello</span><p>World!</p></div>")
    
    def test_to_html_missing_Tag(self):
        no_tag = ParentNode(None, [LeafNode("span", "Oops")])
        with self.assertRaises(ValueError):
            no_tag.to_html()
    
    def test_to_html_Invalid_children(self):
        invalid_child = ParentNode("div", ["I'm not a node"])
        with self.assertRaises(TypeError):
            invalid_child.to_html()
        
        
        


if __name__ == "__main__":
    unittest.main()