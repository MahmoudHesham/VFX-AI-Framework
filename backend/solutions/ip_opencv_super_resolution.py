import os
from tempfile import TemporaryDirectory
from opencv_super_resolution.main import make_image_super_resolution
import utils

def process(received_data:dict) -> dict:
	
	'''
		this function will take input of type dict in a format of {'filename': '', data:''}
		from the client post request to process the included image and then return a dict
		with exact the same format.

	'''

	tempfolder = TemporaryDirectory(dir='workspace')

	filename, ext = os.path.splitext(received_data['filename'])
	output_filename = f'{filename}_output{ext}'

	input_image_filepath = os.path.abspath(os.path.join(tempfolder.name, received_data['filename']))
	output_image_filepath = os.path.abspath(os.path.join(tempfolder.name, output_filename))
	
	input_image = utils.convert_base64_to_file(base64_data=received_data['data'], output_filepath=input_image_filepath)
	
	if(os.path.exists(input_image)):
		make_image_super_resolution(image_input_path=input_image, image_output_path=output_image_filepath)

	else:
		print('Couldn\'t find input image, processing aborted.')
		return None

	if os.path.exists(output_image_filepath):
		return {'filename': output_filename, 'data': utils.convert_file_to_base64(output_image_filepath)}

	print('Processing image failed, please try again.')
	return None