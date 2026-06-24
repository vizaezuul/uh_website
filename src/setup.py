import os
import shutil

def copy_static_to_public(static, public):
	contents = os.listdir(static)
	for item in sorted(contents):
		new_source = os.path.join(static, item)
		new_destination = os.path.join(public, item)
		if os.path.isdir(new_source):
			print(f"Copying {new_destination} directory")
			os.mkdir(new_destination)
			copy_static_to_public(new_source, new_destination)
		else:
			print(f"Copying {new_destination} directory")
			shutil.copyfile(new_source, new_destination)

def main():
	if os.path.exists("public"):	
		print("Deleting /public directory")
		shutil.rmtree("public")
	print("Creating /public directory")
	os.mkdir("public")
	copy_static_to_public("static", "public")

main()
