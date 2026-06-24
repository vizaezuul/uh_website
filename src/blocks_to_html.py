from markdown_blocks import BlockType, markdown_to_blocks, block_to_block_type
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def markdown_to_html_node(markdown):
	blocks = markdown_to_blocks(markdown)
	parentnodes = []
	for block in blocks:
		blocktype = block_to_block_type(block)
		match blocktype:
			case BlockType.PARAGRAPH:
				leafnodes = text_to_children(block)
				tag = "p"
				parentnode = ParentNode(tag, leafnodes)
				parentnodes.append(parentnode)
				#return parentnode
			case BlockType.HEADING:
				n = len(block.split()[0])
				tag = f"h{n}"
				block = block[n+1:]
				leafnodes = text_to_children(block)
				parentnode = ParentNode(tag, leafnodes)
				parentnodes.append(parentnode)
				#return parentnode
			case BlockType.CODE:
				lines = block.split("\n")
				codelines = ""
				for i in range(1, len(lines)-1):
					codelines += lines[i] + "\n"
				leafnode = text_node_to_html_node(TextNode(codelines, TextType.TEXT))
				parentnode = ParentNode("code", [leafnode])
				parentnode = ParentNode("pre", [parentnode])
				parentnodes.append(parentnode)
				#return parentnode
			case BlockType.QUOTE:
				lines = block.split("\n")
				quotelines = ""
				for line in lines:
					line = line.removeprefix(">").removeprefix(" ")
					quotelines += line + "\n"
				leafnodes = text_to_children(quotelines)
				parentnode = ParentNode("blockquote", leafnodes)
				parentnodes.append(parentnode)
				#return parentnode
			case BlockType.ULIST:
				lines = block.split("\n")
				leafnodes = []
				for line in lines:
					line = line[2:]
					leafnode = text_to_children(line)
					wrapped_leaf = ParentNode("li", leafnode)
					leafnodes.append(wrapped_leaf)
				parentnode = ParentNode("ul", leafnodes)
				parentnodes.append(parentnode)
				#return parentnode
			case BlockType.OLIST:
				lines = block.split("\n")
				leafnodes = []
				for line in lines:
					line = line.split(". ",1)[1]
					leafnode = text_to_children(line)
					wrapped_leaf = ParentNode("li", leafnode)
					leafnodes.append(wrapped_leaf)
				parentnode = ParentNode("ol", leafnodes)
				parentnodes.append(parentnode)
				#return parentnode
	
	return ParentNode("div", parentnodes)
	



def text_to_children(text):
	textnodes = text_to_textnodes(text)
	leafnodes = []
	for textnode in textnodes:
		leafnode = text_node_to_html_node(textnode)
		leafnodes.append(leafnode)
	return leafnodes
