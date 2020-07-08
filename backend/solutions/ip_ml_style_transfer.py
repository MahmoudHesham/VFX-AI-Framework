import os
from tempfile import TemporaryDirectory
from ml_style_transfer.main import fast_style_transfer
import utils
import inspect

def process(received_data:dict) -> dict:
	
	'''
		this function will take input of type dict in a format of {'filename': '', data:''}
		from the client post request to process the included image and then return a dict
		with exact the same format.

	'''
	print(received_data)
	print(received_data)
	print(received_data)
	print(received_data)
	tempfolder = TemporaryDirectory(dir='workspace')

	filename, ext = os.path.splitext(received_data['filename'])
	output_filename = f'{filename}_output{ext}'

	input_image_filepath = os.path.abspath(os.path.join(tempfolder.name, received_data['filename']))
	output_image_filepath = os.path.abspath(os.path.join(tempfolder.name, output_filename))
	
	input_image = utils.convert_base64_to_file(base64_data=received_data['data'], output_filepath=input_image_filepath)
	
	if(os.path.exists(input_image)):

		solution_dir = os.path.dirname(inspect.getsourcefile(fast_style_transfer))
		style_model = f"{solution_dir}/models/{received_data['style']}.ckpt"

		fast_style_transfer(image_input_path=input_image, image_output_path=output_image_filepath, style=style_model)

	else:
		print('Couldn\'t find input image, processing aborted.')
		return None

	if os.path.exists(output_image_filepath):
		return {'filename': output_filename, 'data': utils.convert_file_to_base64(output_image_filepath)}

	print('Processing image failed, please try again.')
	return None