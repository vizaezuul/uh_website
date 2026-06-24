from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
	TEXT = "text"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINK = "link"
	IMAGE = "image"

class TextNode():
	def __init__(self, text, text_type, url = None):
		self.text = text
		self.text_type = text_type
		self.url = url

	def __eq__(self, other) -> bool:
		return (
			self.text_type == other.text_type
			and self.text == other.text
			and self.url == other.url
		)
	
	def __repr__(self):
		return f"TextNode({self.text}, {self.text_type}, {self.url})"
	
def text_node_to_html_node(textnode) -> LeafNode:
	match textnode.text_type:
		case TextType.TEXT:
			return LeafNode(None, textnode.text)
		case TextType.BOLD:
			return LeafNode("b", textnode.text)
		case TextType.ITALIC:
			return LeafNode("i", textnode.text)
		case TextType.CODE:
			return LeafNode("code", textnode.text)
		case TextType.LINK:
			return LeafNode("a", textnode.text,{"href": textnode.url})
		case TextType.IMAGE:
			#return LeafNode("img",{"src": textnode.url, "alt": textnode.text}, None)
			return LeafNode("img", "", {"src": textnode.url, "alt": textnode.text})
		case _:
			raise Exception("invalid text type")
