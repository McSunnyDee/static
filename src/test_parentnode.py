import unittest

from parentnode import ParentNode
from leafnode import LeafNode


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
    

    def test_to_html_with_multiple_children(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("b", "child2")
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><b>child2</b></div>")


    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", [])
        try:
            parent_node.to_html()
        except Exception as e:
            self.assertEqual(isinstance(e, ValueError), True)


    def test_to_html_with_multiple_children_and_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        grandchild2_node = LeafNode("a", "grandchild2", {"href": "https://www.google.com"})
        grandchild2_node2 = LeafNode("i", "grandchild3")
        child_node = ParentNode("span", [grandchild_node])
        child_node2 = ParentNode("p", [grandchild2_node, grandchild2_node2])
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span><p><a href=\"https://www.google.com\">grandchild2</a><i>grandchild3</i></p></div>",
        )

if __name__ == "__main__":
    unittest.main()