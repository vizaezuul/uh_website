class HTMLNode:
	def __init__(self, tag = None, value = None, children = None,
		props = None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def to_html(self):
		raise NotImplementedError

	def props_to_html(self):
		if self.props == None or self.props =="":
			return ""
		html_string = ""
		for item in self.props:
			html_string += f' {item}="{self.props[item]}"'
		return html_string

	def __repr__(self):
		return f"tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props}"

class LeafNode(HTMLNode):
	def __init__(self, tag, value, props = None):
		super().__init__(tag, value, None, props)

	def to_html(self):
		if self.value == None:
			raise ValueError("'value' has no value")
		if self.tag == None:
			return self.value
		return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

	def __repr__(self):
		return f"tag: {self.tag}, value: {self.value}, props: {self.props}"

class ParentNode(HTMLNode):
	def __init__(self, tag, children, props = None):
		super().__init__(tag, None, children, props)

	def to_html(self):
		if self.tag == None:
			raise ValueError("Missing tag value!")
		if self.children == None:
			raise ValueError("Missing children! Amber alert!")
		html_string = f"<{self.tag}{self.props_to_html()}>"
		for child in self.children:
			html_string += child.to_html()
		html_string += f"</{self.tag}>"
		return html_string
		
