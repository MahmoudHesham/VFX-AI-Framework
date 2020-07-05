import requests
import utils


post_json_data = {
	"filename":"cat.jpg",
	"data": utils.convert_image_to_base64("cat.jpg")
}

req = requests.post("http://127.0.0.1:5000/image_processing/gray", json=post_json_data)

req_result = req.json()

utils.convert_base64_to_image(base64_data=req_result["data"], output_file=req_result["filename"])
