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
        
        src_image_loader_layout = QtWidgets.QVBoxLayout()

        self.src_image_placeholder = QtWidgets.QLabel()
        self.load_src_image_btn = QtWidgets.QPushButton("Load Source Image")
        self.load_src_image_btn.clicked.connect(self.load_src_image_fn)

        src_image_loader_layout.addWidget(self.src_image_placeholder, 0, QtCore.Qt.AlignCenter)
        src_image_loader_layout.addWidget(self.load_src_image_btn)

        style_image_loader_layout = QtWidgets.QHBoxLayout()

        styles_dir = f'{os.path.dirname(os.path.realpath(__file__))}/data/style_transfer/styles'
        styles = [os.path.join(styles_dir, x) for x in os.listdir(styles_dir)]

        self.styles_btns = []
        
        for style in styles:
            style_name = os.path.basename(style)[:-4]

            style_btn = QtWidgets.QToolButton()
            style_btn.setCheckable(True)
            style_btn.setAutoRaise(True)
            style_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
            style_btn.setText(style_name)
            style_btn.setIcon(QtGui.QIcon(QtGui.QPixmap(style)))
            style_btn.setIconSize(QtCore.QSize(90,90))
            style_btn.clicked.connect(self.change_style)

            style_image_loader_layout.addWidget(style_btn)
            
            self.styles_btns.append(style_btn)

        self.request_body['style'] = self.styles_btns[0].text()
        self.styles_btns[0].setChecked(True)

        self.layout().addLayout(src_image_loader_layout)
        self.layout().addLayout(style_image_loader_layout)

    def change_style(self):

        for btn in self.styles_btns:
            btn.setChecked(False)

        selected_style = self.sender()
        selected_style.setChecked(True)
        self.request_body['style'] = selected_style.text()

    def load_src_image_fn(self):

        image_file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select source image", None, "Images (*.png *.tiff *.jpg)")

        if(image_file):
            self.src_image_placeholder.setPixmap(QtGui.QPixmap(image_file).scaled(250, 250, QtCore.Qt.KeepAspectRatio))
            self.request_body = {'filename': os.path.basename(image_file), 'data': utils.convert_file_to_base64(image_file)}

    def recived_data_handler(self, response, output):

        current_time = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
        session_output = os.path.join(output, current_time)
        os.mkdir(session_output)
        utils.convert_base64_to_file(base64_data=response['data'], output_filepath=os.path.join(session_output, response['filename']))