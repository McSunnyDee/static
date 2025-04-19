import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "text in paragraph")
        node2 = HTMLNode("p", "text in paragraph")
        self.assertEqual(node, node2)
        
    def test_eq_raw_text(self):
        node = HTMLNode("raw text")
        node2 = HTMLNode("raw text")
        self.assertEqual(node, node2)

    def test_neq_raw_text(self):
        node = HTMLNode("raw text")
        node2 = HTMLNode()
        self.assertNotEqual(node, node2)
        
    def test_eq_props(self):
        node = HTMLNode(None, None, None, {"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node.props_to_html(), f" href=\"https://www.google.com\" target=\"_blank\"")
    
    def test_eq_repr(self):
        node = HTMLNode(None, None, None, {"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(repr(node), f"tag=\"None\"; value=\"None\"; children=\"None\"; props=\" href=\"https://www.google.com\" target=\"_blank\"\"")

if __name__ == "__main__":
    unittest.main()