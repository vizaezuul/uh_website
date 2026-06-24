import unittest
from htmlnode import HTMLNode

node = HTMLNode(tag = "a", value="What up?", props={"class": "text-large"})
print(node)

