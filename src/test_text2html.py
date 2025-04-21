import unittest

from text2html import (
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images
)
from textnode import TextNode, TextType


class TestText2LeafNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")


    def test_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")


    def test_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")

    
    def test_link(self):
        node = TextNode("This is a link text node", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertEqual(html_node.props, {"href": "https://www.google.com",})


    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://www.imagewebsite.com/foo.jpeg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.imagewebsite.com/foo.jpeg", "alt": "This is an image node",})


    def test_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, 
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )
    
    def test_two_delimiters(self):
        node = TextNode("This is text with a `code block` word and another `code block`, too", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, 
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word and another ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(", too", TextType.TEXT),
            ]
        )

    def test_end_with_delimiter(self):
        node = TextNode("This is text with a `code block` word and another `code block, too`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, 
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word and another ", TextType.TEXT),
                TextNode("code block, too", TextType.CODE),
                TextNode("", TextType.TEXT),
            ]
        )

    def test_start_and_end_with_delimiter(self):
        node = TextNode("`This` is text with a `code block` word and another `code block, too`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, 
            [
                TextNode("", TextType.TEXT),
                TextNode("This", TextType.CODE),
                TextNode(" is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word and another ", TextType.TEXT),
                TextNode("code block, too", TextType.CODE),
                TextNode("", TextType.TEXT),
            ]
        )

    def test_more_than_one_transformation(self):
        node = TextNode("`This` is **text** with a `code block` word and _another_ `code block, too`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertEqual(new_nodes, 
            [
                TextNode("", TextType.TEXT),
                TextNode("This", TextType.CODE),
                TextNode(" is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("code block, too", TextType.CODE),
                TextNode("", TextType.TEXT),
            ]
        )
    
    def test_multiple_transformations_with_different_order(self):
        node = TextNode("`This` is **text** with a `code block` word and _another_ `code block, too`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, 
            [
                TextNode("", TextType.TEXT),
                TextNode("This", TextType.CODE),
                TextNode(" is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("code block, too", TextType.CODE),
                TextNode("", TextType.TEXT),
            ]
        )

    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [hyperlink](https://google.com)"
        )
        self.assertListEqual([("hyperlink", "https://google.com")], matches)


    def test_extract_multiple_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [hyperlink](https://google.com) and this is [another](https://bettergoogle.com)"
        )
        self.assertListEqual([("hyperlink", "https://google.com"), ("another", "https://bettergoogle.com"),], matches)


    def test_dont_think_image_is_link(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertNotEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


if __name__ == "__main__":
    unittest.main()