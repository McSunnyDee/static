import re
from textnode import TextNode, TextType
from text2html import extract_markdown_images, extract_markdown_links, text_to_textnodes, block_to_block_type, markdown_to_html_node

def main():
    #dummy = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    #print(dummy)
    #nodes = text_to_textnodes(r"This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
    #print(nodes)
    #block = ">one\n>two\nthree"
    #print(list((r"^\>.+", line) for line in block.split("\n")))
    #print(
    #    list(
    #        filter(
    #            lambda x: re.findall(r"^\>.*", x), (line for line in block.split("\n"))
    #        )
    #    )
    #)
    #print(block_to_block_type(block))
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    print(html)


main()