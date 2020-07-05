import os
import base64

def convert_file_to_base64(filepath:str) -> str:
	'''
	:param str filepath: the path of the file that will be converted into base64 format.
	
	this function takes filepath as input and return a string 
	representing the file data in base64 format.
	
	'''

	if os.path.exists(filepath):
		with open(filepath, 'rb') as file:
			return base64.b64encode(file.read()).decode('utf-8')

	print('Couldn\'t find the input file. conversion aborted.')
	return None

def convert_base64_to_file(base64_data:str, output_filepath:str) -> str:
	'''
	:param str base64_data: the base64 data that is going to be converted into a file.
	:param str output_filepath: the output path of the converted base64 data into file.

	this function takse base64 data as input and ouput path where it's going to be decoded into.
	and returns the output filepath if the decoding has succeeded.
	'''

	if base64_data:
		with open(output_filepath, 'wb') as file:
			file.write(base64.b64decode(base64_data))

		return output_filepath
		
	else:
		print('The input base64 data is empty. conversion aborted.')
		return None
