import os
import base64

def convert_image_to_base64(image_path:str) -> str:

	if os.path.exists(image_path):
		with open(image_path, "rb") as img_file:
			return base64.b64encode(img_file.read())

	return None

def convert_base64_to_image(base64:str, output_file:str) -> str:

	with open(output_file, "wb") as img_file:
		return base64.b64decode(base64)

	return None