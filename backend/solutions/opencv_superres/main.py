import os
import cv2

def make_image_superres(image_input_path:str, image_output_path:str) -> str:

	'''
	:param str image_input_path: The path of the input image.
	:param str image_output_path: The path of the output image.

	this is a basic function to double-upscale input image
	and save it into output file.

	'''

	if os.path.exists(image_input_path):
		cv_img = cv2.imread(image_input_path)
		height, width = img.shape[:2]
		
		resized_cv_img = cv2.resize(cv_img, (2*width, 2*height), interpolation = cv2.INTER_CUBIC)
		cv2.imwrite(image_output_path, resized_cv_img)

	else:
		print('Couldn\'t find input image, conversion aborted.')		
		return None

	return image_output_path