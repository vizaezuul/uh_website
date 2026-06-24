from enum import Enum
from textnode import TextNode, TextType
import re

class BlockType(Enum):
	PARAGRAPH = "paragraph"
	HEADING = "heading"
	CODE = "code"
	QUOTE = "quote"
	ULIST = "unordered_list"
	OLIST = "ordered_list"

def markdown_to_blocks(text: str) -> list[str]:
	blocks = text.split("\n\n")
	stripped_blocks = []
	for block in blocks:
		stripped_block = block.strip()
		if stripped_block != "":
			stripped_blocks.append(stripped_block)
	return stripped_blocks

def block_to_block_type(text: str) -> BlockType:
	first_word = text.split()[0]
	first_character = first_word[0]
	match first_character:
		case "#":
			for i, ch in enumerate(first_word):
				if ch != "#" or i > 5:
					return BlockType.PARAGRAPH
			if text[len(first_word)] != " ":
				return BlockType.PARAGRAPH
			return BlockType.HEADING
					
	
		case "`":
			lines = text.split("\n")
			if lines[0] == "```" and lines[-1] == "```":
				return BlockType.CODE
			return BlockType.PARAGRAPH

		case ">":
			lines = text.split("\n")
			for line in lines:
				if not line.startswith(">"):
					return BlockType.PARAGRAPH
			return BlockType.QUOTE

		case "-":
			lines = text.split("\n")
			for line in lines:
				if not line.startswith("- "):
					return BlockType.PARAGRAPH
			return BlockType.ULIST

		case "1":
			lines = text.split("\n")
			for i, line in enumerate(lines):
				if not line.startswith(f"{i + 1}. "):
					return BlockType.PARAGRAPH
			return BlockType.OLIST

		case _:
			return BlockType.PARAGRAPH

