from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

@app.route('/')
def index():
	return "baby steps to ai, VFX Kitchen."

@app.route('/image_processing/gray', methods=['POST'])
def gray_image_processing():

	received_data = request.json

	print("here happens all the ai magic")

	result = "output data"
	return jsonify({"received_data": result})

if __name__ == "__main__":
	app.run(debug=True)