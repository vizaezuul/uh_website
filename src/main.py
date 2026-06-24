from textnode import TextNode
from blocks_to_html import markdown_to_html_node
#from htmlnode import HTMLNode, LeafNode, ParentNode
import os
import shutil

def copy_static_to_public(static, public):
	contents = os.listdir(static)
	for item in sorted(contents):
		new_source = os.path.join(static, item)
		new_destination = os.path.join(public, item)
		if os.path.isdir(new_source):
			print(f"Creating {new_destination} directory")
			os.mkdir(new_destination)
			copy_static_to_public(new_source, new_destination)
		else:
			print(f"Copying {new_source} to {new_destination}")
			shutil.copyfile(new_source, new_destination)

def extract_title(markdown):
	title = ""
	markdown_list = markdown.split("\n")
	for line in markdown_list:
		if line[0:2] == "# ":
			title = line.lstrip(" #")
			break
	#	raise Exception(f"No header found in {markdown}")
	return(title)
	
def generate_page(from_path, template_path, dest_path):
	print(f"Conjuring page from {from_path} to {dest_path} using {template_path}")
	with open(from_path, "r") as f:
		markdown = f.read()
	with open(template_path, "r") as f:
		template = f.read()
	markdown_blocks = markdown_to_html_node(markdown)
	content = markdown_blocks.to_html()
	title = extract_title(markdown)
	template = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
	verify_directory = "/".join(dest_path.split("/")[0:-1])
	if not os.path.exists(verify_directory):
		os.mkdir(verify_directory)
	with open(dest_path, "a") as f:
		f.write(template)
	
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
	if not os.path.exists(dir_path_content):
		raise Exception(f"No content found in {dir_path_content}")
	contents = os.listdir(dir_path_content)
	for content in contents:
		new_source = os.path.join(dir_path_content, content)
		if os.path.isdir(new_source):
			new_destination = os.path.join(dest_dir_path, content)
			print(f"Creating new directory: {new_destination}")
			os.mkdir(new_destination)
			generate_pages_recursive(new_source, template_path, new_destination)
		else:
			content = str(content.split(".")[0]) + ".html"	
			new_destination = os.path.join(dest_dir_path, content)

			print(f"Copying {new_source} to {new_destination}...")
			generate_page(new_source, template_path, new_destination)
	print(contents)



def main():
	if os.path.exists("public"):
		print("Deleting /public directory")
		shutil.rmtree("public")
	print("Creating /public directory")
	os.mkdir("public")
	copy_static_to_public("static", "public")
	generate_pages_recursive("./content", "./template.html", "./public")


main()

