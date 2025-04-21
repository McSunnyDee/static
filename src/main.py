from textnode import TextNode, TextType
from text2html import extract_markdown_images, extract_markdown_links

def main():
    #dummy = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    #print(dummy)
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    print(extract_markdown_links(text))


main()