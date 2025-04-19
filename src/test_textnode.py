import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_eq_no_url(self):
        node3 = TextNode("This is a text node", TextType.LINK, None)
        node4 = TextNode("This is a text node", TextType.LINK)
        self.assertEqual(node3, node4)

    def test_neq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node2", TextType.BOLD)
        self.assertNotEqual(node, node2)
        
    def test_neq_type(self):
        node3 = TextNode("This is a text node", TextType.ITALIC)
        node4 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node3, node4)
    
    def test_neq_url(self):
        node5 = TextNode("This is a text node", TextType.IMAGE, "www.boot.dev")
        node6 = TextNode("This is a text node", TextType.IMAGE, "www.boot.dev/light")
        self.assertNotEqual(node5, node6)

if __name__ == "__main__":
    unittest.main()