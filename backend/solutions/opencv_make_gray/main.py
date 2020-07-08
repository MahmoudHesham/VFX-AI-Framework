import os
import cv2

def make_image_gray(image_input_path:str, image_output_path:str) -> str:

	'''
	:param str image_input_path: The path of the input image.
	:param str image_output_path: The path of the output image.

	this is a basic function to convert input image to gray
	and save it into output file.

	'''
	if os.path.exists(image_input_path):
		cv_gray_img = cv2.imread(image_input_path, 0)
		cv2.imwrite(image_output_path, cv_gray_img)

	else:
		print('Couldn\'t find input image, conversion aborted.')		
		return None

	return image_output_path