import sys

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

import utils

class MainWidget(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super(MainWidget, self).__init__(parent=parent)

		self.setLayout(QtWidgets.QVBoxLayout())

		self.src_img_placeholder = QtWidgets.QLabel("source image")
		self.load_image_btn = QtWidgets.QPushButton("Load Image")

		self.load_image_btn.clicked.connect(self.load_image_fn)


		self.layout().addWidget(self.src_img_placeholder)
		self.layout().addWidget(self.load_image_btn)

	def load_image_fn(self):

		filename, _ = QtWidgets.QFileDialog.getOpenFileName(self)

		if filename:
			self.src_img_placeholder.setPixmap(QtGui.QPixmap(filename))

			img_b64 = utils.convert_image_to_base64(filename)
			print(img_b64)


class HelloClient(QtWidgets.QMainWindow):
	def __init__(self, parent=None):
		super(HelloClient, self).__init__(parent=parent)

		main_widget = MainWidget()

		self.setCentralWidget(main_widget)


if __name__ == "__main__":

	app = QtWidgets.QApplication(sys.argv)

	hello_client = HelloClient()
	hello_client.show()