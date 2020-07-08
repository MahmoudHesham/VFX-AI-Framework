import os
from datetime import datetime

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

import utils

'''
custom plugin guideline
=========================
** these guidelines are still work in progress and might be updated later. **

Plugin class should be called Register.
Plugin class should have 'request_body' variable that includes the post request data.
Plugin class should have recived_data_handler() function to store the output data in the specified output parameter.
'''

class Register(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(Register, self).__init__(parent=parent)
        self.request_body = {}
        
        self.init_ui()

    def init_ui(self):

        self.setLayout(QtWidgets.QVBoxLayout())
        
        self.image_placeholder = QtWidgets.QLabel()
        self.load_image_btn = QtWidgets.QPushButton("Load Image")
        self.load_image_btn.clicked.connect(self.load_image_fn)

        self.layout().addWidget(self.image_placeholder)
        self.layout().addWidget(self.load_image_btn)

    def load_image_fn(self):

        image_file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select source image", None, "Images (*.png *.tiff *.jpg)")

        if(image_file):
            self.image_placeholder.setPixmap(QtGui.QPixmap(image_file))
            self.request_body = {'filename': os.path.basename(image_file), 'data': utils.convert_file_to_base64(image_file)}

    def recived_data_handler(self, response, output):

        current_time = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
        session_output = os.path.join(output, current_time)
        os.mkdir(session_output)
        utils.convert_base64_to_file(base64_data=response['data'], output_filepath=os.path.join(session_output, response['filename']))