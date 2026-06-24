import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks

class TestTextNode(unittest.TestCase):
	def test_markdown_to_blocks(self):
		md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
		blocks = markdown_to_blocks(md)
		should_be = ["This is **bolded** paragraph", "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line", "- This is a list\n- with items"]
		self.assertListEqual(should_be, blocks)

#------------------------------------------

	def test_different_markdown_to_blocks(self):
		md = """
# This is a heading



This is a paragraph of text. It has some **bold** abd _italic_ and `code` words in it.
This is a new line in the same paragraph.

- This is a first list item in a list block
- This is a list item
- This is another list item
"""
		blocks = markdown_to_blocks(md)
		should_be = ["# This is a heading", "This is a paragraph of text. It has some **bold** abd _italic_ and `code` words in it.\nThis is a new line in the same paragraph.", "- This is a first list item in a list block\n- This is a list item\n- This is another list item"]
		self.assertListEqual(should_be, blocks)

#---------------------------------------

if __name__ == "__main__":
	unittest.main()
