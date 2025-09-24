import unittest

from text2html import (
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node
)
from textnode import TextNode, TextType, BlockType


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
                #TextNode("", TextType.TEXT),
            ]
        )

    def test_start_and_end_with_delimiter(self):
        node = TextNode("`This` is text with a `code block` word and another `code block, too`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, 
            [
                #TextNode("", TextType.TEXT),
                TextNode("This", TextType.CODE),
                TextNode(" is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word and another ", TextType.TEXT),
                TextNode("code block, too", TextType.CODE),
                #TextNode("", TextType.TEXT),
            ]
        )

    def test_more_than_one_transformation(self):
        node = TextNode("`This` is **text** with a `code block` word and _another_ `code block, too`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertEqual(new_nodes, 
            [
                #TextNode("", TextType.TEXT),
                TextNode("This", TextType.CODE),
                TextNode(" is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("code block, too", TextType.CODE),
                #TextNode("", TextType.TEXT),
            ]
        )
    
    def test_multiple_transformations_with_different_order(self):
        node = TextNode("`This` is **text** with a `code block` word and _another_ `code block, too`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, 
            [
                #TextNode("", TextType.TEXT),
                TextNode("This", TextType.CODE),
                TextNode(" is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("code block, too", TextType.CODE),
                #TextNode("", TextType.TEXT),
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


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    
    def test_starts_with_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )


    def test_ends_with_text(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and that's it!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" and that's it!", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_one_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )


    def test_no_images(self):
        node = TextNode(
            "This is text without an image",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text without an image", TextType.TEXT),
            ],
            new_nodes,
        )

    
    def test_link_is_not_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/3elNhQu.png) and a [hyperlink](https://google.com) and that's it!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" and a [hyperlink](https://google.com) and that's it!", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_image_is_not_link(self):
        node = TextNode(
            "This is text with a [hyperlink](https://google.com) and an ![image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("hyperlink", TextType.LINK, "https://google.com"),
                TextNode(" and an ![image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_all_of_them_at_the_same_time(self):
        nodes = text_to_textnodes(r"This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )
    

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_block_to_blocktype_heading(self):
        test_block = [
            "# This is a Header",
            "## This is a Header",
            "### This is a Header",
            "#### This is a Header",
            "##### This is a Header",
            "###### This is a Header",
            "####### This is a Header",
            "#This is a Header",
            "##This is a Header",
            "###This is a Header",
            "####This is a Header",
            "#####This is a Header",
            "######This is a Header",
            "#######This is a Header",
            "This is a Header",
            "#"
            "# "
            
        ]
        results = [
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
        ]
        self.assertListEqual(list(map(block_to_block_type, test_block)), results)
    
    def test_block_to_blocktype_code(self):
        test_block = [
            "```This is Code```",
            "``` This is Code ```",
            "`` `This is Code```",
            "```This is Code` ``",
            "``This is Code``",
            "```This is Code``",
            "This is Code",
            "``````",
            "``` ```",
            "```` ``",
        ]
        results = [
            BlockType.CODE,
            BlockType.CODE,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.CODE,
            BlockType.CODE,
            BlockType.PARAGRAPH,
        ]
        self.assertListEqual(list(map(block_to_block_type, test_block)), results)
    

    def test_block_to_blocktype_quote(self):
        self.assertEqual(block_to_block_type(">one\n>two\n>three"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">one"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">one\n>two\nthree"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(">one\ntwo\n>three"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("one\n>two\n>three"), BlockType.PARAGRAPH)

    
    def test_block_to_blocktype_unordered_list(self):
        self.assertEqual(block_to_block_type("- one\n- two\n- three"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- one"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- "), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- one\n- two\nthree"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("- one\n- two\n three"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("- one\ntwo\n- three"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("one\n- two\n- three"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("-one\n- two\n- three"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("- one\n- two\n-three"), BlockType.PARAGRAPH)


    def test_block_to_blocktype_ordered_list(self):
        self.assertEqual(block_to_block_type("1. one\n2. two\n3. three"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. one"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. "), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1."), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1. 2. 3."), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. one\n2. two\n3 three"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1. one\n2. two\n3.. three"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1. one\ntwo\n2. three"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("one\n1. two\n2. three"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1.one\n2.two\n3.three"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1. one\n3. two\n2. three"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("0. one\n1. two\n2. three"), BlockType.PARAGRAPH)


    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()