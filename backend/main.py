from flask import Flask
from flask import request
from flask import jsonify

import solutions

ml_solutions = solutions.MLSolutions()
app = Flask(__name__)

@app.route('/')
def index():
	return "baby steps to ai, VFX Kitchen."

@app.route('/image_processing/gray', methods=['POST'])
def gray_image_processing():

	received_data = request.json
	processed_data = ml_solutions.ip_opencv_make_gray.process(received_data)

	return jsonify(processed_data)

@app.route('/image_processing/superres', methods=['POST'])
def superres_image_processing():

	received_data = request.json
	processed_data = ml_solutions.ip_opencv_superres.process(received_data)

	return jsonify(processed_data)

if __name__ == "__main__":
	app.run(debug=True)