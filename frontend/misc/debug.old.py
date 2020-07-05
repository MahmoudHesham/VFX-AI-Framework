import sys
sys.path.append("..")

import requests
import utils

post_json_data = {
	"filename": "cat.jpg",
	"data": utils.convert_file_to_base64("cat.jpg")
}

# req = requests.post("http://127.0.0.1:5000/image_processing/gray", json=post_json_data)
req = requests.post("http://127.0.0.1:5000/image_processing/superres", json=post_json_data)
req_result = req.json()

utils.convert_base64_to_file(base64_data=req_result["data"], output_filepath=req_result["filename"])