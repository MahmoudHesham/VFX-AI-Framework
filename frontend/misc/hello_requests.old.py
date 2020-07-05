import requests
import os
import cv2
import tempfile

req = requests.get("http://www.splashbase.co/api/v1/images/random")

if(req.status_code == 200):

    img_url = req.json()["url"]
    img_req = requests.get(img_url)

    if(img_req.status_code == 200):

        tempfolder = tempfile.TemporaryDirectory(dir="workspace")

        img_filename = os.path.basename(img_url)
        img_downloaded = os.path.join(tempfolder.name, img_filename)
        
        with open(img_downloaded, "wb") as f:
            f.write(img_req.content)

        filename, ext = os.path.splitext(img_downloaded)

        cv_img = cv2.imread(img_downloaded, 0)
        cv2.imwrite("{filename}_gray{ext}".format(filename=filename, ext=ext), cv_img)