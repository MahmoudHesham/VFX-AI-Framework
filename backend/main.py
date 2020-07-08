from flask import Flask
from flask import request
from flask import jsonify

import solutions

ml_solutions = solutions.MLSolutions()
app = Flask(__name__)

@app.route('/')
def index():
	return "baby steps to ai, VFX Kitchen."

@app.route('/image_processing/grayscale', methods=['POST'])
def gray_image_processing():

	received_data = request.json
	processed_data = ml_solutions.ip_opencv_make_gray.process(received_data)

	return jsonify(processed_data)

@app.route('/image_processing/super_resolution', methods=['POST'])
def super_resolution_image_processing():

	received_data = request.json
	processed_data = ml_solutions.ip_opencv_super_resolution.process(received_data)

	return jsonify(processed_data)

@app.route('/image_processing/style_transfer', methods=['POST'])
def style_transfer_image_processing():

	received_data = request.json
	processed_data = ml_solutions.ip_ml_style_transfer.process(received_data)

	return jsonify(processed_data)

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)