import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")


    def test_no_value_given(self):
        try:
            node = LeafNode("p")
        except Exception as e:
            self.assertEqual(str(e), "LeafNode.__init__() missing 1 required positional argument: 'value'")


    def test_value_eq_none(self):
        node = LeafNode("p", None)
        try:
            print(node.to_html())
        except Exception as e:
            self.assertEqual(isinstance(e, ValueError), True)


    def test_no_tag_given(self):
        try:
            node = LeafNode(value="no tag given")
        except Exception as e:
            self.assertEqual(str(e), "LeafNode.__init__() missing 1 required positional argument: 'tag'")


    def test_tag_eq_none(self):
        node = LeafNode(None, "tag is none")
        self.assertEqual(node.to_html(), "tag is none")


if __name__ == "__main__":
    unittest.main()