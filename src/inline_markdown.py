from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
	new_nodes = []
	for node in old_nodes:
		if node.text_type != TextType.TEXT:
			new_nodes.append(node)
		else:
			split_node = node.text.split(delimiter)
			if len(split_node) % 2 == 0:
				raise Exception(f"unclosed tag in {node.text},{node.text_type}")
			else:
				for i, string in enumerate(split_node):
					if string != "":
						if i % 2 == 0:
							texttype = TextType.TEXT
						else:
							texttype = text_type
						new_nodes.append(TextNode(string, texttype))

	return new_nodes

def extract_markdown_images(text):
	images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)	
	return images

def extract_markdown_links(text):
	links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
	return links

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
	new_nodes = []
	for node in old_nodes:
		if node.text_type != TextType.TEXT:
			new_nodes.append(node)
		else:
			images = extract_markdown_images(node.text)
			if len(images) == 0:
				new_nodes.append(node)
			else:
				remaining_text = node.text
				for image in images:
					image_string = f"![{image[0]}]({image[1]})"
					sections = remaining_text.split(image_string)
					if sections[0] != "":
						new_node = TextNode(sections[0], TextType.TEXT)
						new_nodes.append(new_node)
					image_node = TextNode(image[0], TextType.IMAGE, image[1])
					new_nodes.append(image_node)
					remaining_text = sections[1]
				if remaining_text != "":
					new_node = TextNode(remaining_text, TextType.TEXT)	
					new_nodes.append(new_node)
	return new_nodes
		



def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
	new_nodes = []
	for node in old_nodes:
		if node.text_type != TextType.TEXT:
			new_nodes.append(node)
		else:
			links = extract_markdown_links(node.text)
			if len(links) == 0:
				new_nodes.append(node)
			else:
				remaining_text = node.text
				for link in links:
					link_string = f"[{link[0]}]({link[1]})"
					sections = remaining_text.split(link_string)
					if sections[0] != "":
						new_node = TextNode(sections[0], TextType.TEXT)
						new_nodes.append(new_node)
					link_node = TextNode(link[0], TextType.LINK, link[1])
					new_nodes.append(link_node)
					remaining_text = sections[1]
				if remaining_text != "":
					new_node = TextNode(remaining_text, TextType.TEXT)
					new_nodes.append(new_node)
	return new_nodes

def text_to_textnodes(text) -> list[TextNode]:
	text_node_list = [TextNode(text, text_type = TextType.TEXT)]
	text_node_list = split_nodes_delimiter(text_node_list, "**", TextType.BOLD)
	text_node_list = split_nodes_delimiter(text_node_list, "_", TextType.ITALIC)
	text_node_list = split_nodes_delimiter(text_node_list, "`", TextType.CODE)
	text_node_list = split_nodes_image(text_node_list)
	text_node_list = split_nodes_link(text_node_list)
	return text_node_list
