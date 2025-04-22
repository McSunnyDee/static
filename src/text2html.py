import re

from textnode import TextType, TextNode
from leafnode import LeafNode

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text,})
        case _:
            raise Exception("Invalid TextType")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        elif len(node.text.split(delimiter)) % 2 == 0:
            raise Exception("Invalid amount of delimeters")
        else:
            for i, words in enumerate(node.text.split(delimiter)):
                if words == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(words, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(words, text_type))

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    #sets would mess with the order and duplicate links
    includes_images = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    images_only = extract_markdown_images(text)
    return [link for link in includes_images if link not in images_only]


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        diminishing_original_text = old_node.text
        extracted_images = extract_markdown_images(diminishing_original_text)
        if len(extracted_images) > 0:
            for image_alt_name, image_link in extracted_images:
                before_and_after = diminishing_original_text.split(f"![{image_alt_name}]({image_link})", 1)
                if len(before_and_after) != 2:
                    raise ValueError("invalid image markdown")
                if before_and_after[0] != "":
                    new_nodes.append(TextNode(before_and_after[0], TextType.TEXT))
                new_nodes.append(TextNode(image_alt_name, TextType.IMAGE, image_link))
                diminishing_original_text = before_and_after[1]
            if diminishing_original_text != "":
                new_nodes.append(TextNode(diminishing_original_text, TextType.TEXT))
        else:
            new_nodes.append(old_node)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        diminishing_original_text = old_node.text
        extracted_links = extract_markdown_links(diminishing_original_text)
        if len(extracted_links) > 0:
            for text, url in extracted_links:
                before_and_after = diminishing_original_text.split(f"[{text}]({url})", 1)
                if len(before_and_after) != 2:
                    raise ValueError("invalid link markdown")
                if before_and_after[0] != "":
                    new_nodes.append(TextNode(before_and_after[0], TextType.TEXT))
                new_nodes.append(TextNode(text, TextType.LINK, url))
                diminishing_original_text = before_and_after[1]
            if diminishing_original_text != "":
                new_nodes.append(TextNode(diminishing_original_text, TextType.TEXT))
        else:
            new_nodes.append(old_node)
    return new_nodes


def text_to_textnodes(text):
    new_nodes = []
    node = [TextNode(text, TextType.TEXT)]
    new_nodes.extend(
        split_nodes_delimiter(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_image(
                        split_nodes_link(node)
                    ), "`", TextType.CODE
                ), "_", TextType.ITALIC
            ), "**", TextType.BOLD
        )
    )
    return new_nodes
