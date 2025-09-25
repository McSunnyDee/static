import os
import pathlib
import re

from textnode import TextType, TextNode, BlockType
from leafnode import LeafNode
from parentnode import ParentNode
from htmlnode import HTMLNode

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


def markdown_to_blocks(markdown):
    md = []
    for block in markdown.split("\n\n"):
        block = block.strip()
        if block != "":
            md.append(block)
    return md


def block_to_block_type(block):
    if re.findall(r"^\#{1,6} .+", block):
        return BlockType.HEADING
    elif len(list(filter(lambda x: re.findall(r"^\`\`\`.*", x), (line for line in block.split("\n"))))) > 0 and len(list(filter(lambda x: re.findall(r".*\`\`\`$", x), (line for line in block.split("\n"))))) > 0:
        return BlockType.CODE
    elif len(list(filter(lambda x: re.findall(r"^\>.*", x), (line for line in block.split("\n"))))) == len(block.split("\n")):
        return BlockType.QUOTE
    elif len(list(filter(lambda x: re.findall(r"^\- .*", x), (line for line in block.split("\n"))))) == len(block.split("\n")):
        return BlockType.UNORDERED_LIST
    elif len(list(filter(lambda args: re.findall(fr"^{args[0]+1}\. .*", args[1]), ((number, line) for number, line in enumerate(block.split("\n")))))) == len(block.split("\n")):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    

def text_to_children(text):
    htmlnodes = []
    for textnode in text_to_textnodes(" ".join(text.split("\n"))):
        htmlnodes.append(text_node_to_html_node(textnode))
    return htmlnodes


def header_size(block):
    size = 0
    for char in block:
        if char == "#":
            size = size + 1
        else:
            return size
        

def resolve_blockquote(block):
    new_lines = []
    for quote_line in block.split("\n"):
        new_lines.append(quote_line[1:].strip())

    return text_to_children("\n".join(new_lines))


def resolve_unordered_lists(block):
    nodes_list = []
    for list_entry in block.split("\n"):
        entry = text_to_children(list_entry[2:])
        nodes_list.append(ParentNode("li", entry))

    return nodes_list


def resolve_ordered_lists(block):
    nodes_list = []
    for list_entry in block.split("\n"):
        entry = text_to_children(list_entry[3:])
        nodes_list.append(ParentNode("li", entry))
    
    return nodes_list


def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    parent_html_node = ParentNode("div", [])
    for block in markdown_blocks:
        match block_to_block_type(block):
            case BlockType.HEADING:
                size = header_size(block)
                parent_html_node.children.append(ParentNode(f"h{size}", text_to_children(block[size+1:])))
            case BlockType.CODE:
                parent_html_node.children.append(
                    ParentNode("pre", [text_node_to_html_node(TextNode(block.replace("```\n", "").replace("```", ""), TextType.CODE))])
                )
            case BlockType.QUOTE:
                parent_html_node.children.append(ParentNode("blockquote", resolve_blockquote(block)))
            case BlockType.UNORDERED_LIST:
                parent_html_node.children.append(ParentNode("ul", resolve_unordered_lists(block)))
            case BlockType.ORDERED_LIST:
                parent_html_node.children.append(ParentNode("ol", resolve_ordered_lists(block)))
            case BlockType.PARAGRAPH:
                parent_html_node.children.append(ParentNode("p", text_to_children(block)))
            case _:
                raise Exception("Invalid BlockType")
    
    return parent_html_node


def extract_title(markdown):
    header = ""
    for block in markdown_to_blocks(markdown):
        if block_to_block_type(block) == BlockType.HEADING:
            header = block
            size = header_size(header)
            return (header[size:]).strip()
    if header == "":
        raise Exception("No Header Found")
    

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        from_path_content = file.read()
    
    with open(template_path) as file2:
        template_path_content = file2.read()

    title = extract_title(from_path_content)
    content = markdown_to_html_node(from_path_content)
    content = content.to_html()
    print(content)

    template_path_content = template_path_content.replace(r"{{ Title }}", title).replace(r"{{ Content }}", content).replace(r'href="/', fr'href="{basepath}').replace(r'src="/', fr'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as file3:
        file3.write(template_path_content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if os.path.exists(dir_path_content) and not os.path.isfile(dir_path_content):
        if not os.path.exists(dest_dir_path):
            os.mkdir(dest_dir_path)
        for file_or_folder in os.listdir(dir_path_content):
            if not os.path.isfile(os.path.join(dir_path_content, file_or_folder)):
                os.mkdir(os.path.join(dest_dir_path, file_or_folder))
                generate_pages_recursive(os.path.join(dir_path_content, file_or_folder), template_path, os.path.join(dest_dir_path, file_or_folder), basepath)
            else:
                if file_or_folder == "index.md":
                    generate_page(os.path.join(dir_path_content, file_or_folder), template_path, os.path.join(dest_dir_path, f'{file_or_folder[:-3]}.html'), basepath)

    else:
        if file_or_folder == "index.md":
            generate_page(os.path.join(dir_path_content), template_path, os.path.join(f'{dest_dir_path[:-3]}.html'))