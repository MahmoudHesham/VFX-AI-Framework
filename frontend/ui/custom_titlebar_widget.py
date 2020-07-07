from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

import webbrowser

class WindowTitleButton(QtWidgets.QPushButton):
    
    def __init__(self, parent = None):
        super(WindowTitleButton, self).__init__(parent)
        self.setFixedSize(15, 15)
        self.setStyleSheet("QPushButton:hover{background-color:orange}\
                            QPushButton{border:1px solid orange}")

class WindowTitleBar(QtWidgets.QWidget):

    def __init__(self, parent = None):
        super(WindowTitleBar, self).__init__(parent=parent)
        
        self._parent = parent
        self.old_pos = self._parent.pos()
        self.maximized = False

        self.init_ui()
    
    def init_ui(self):

        self.setMaximumHeight(20)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(5, 5, 5, 5)
        self.layout().setSpacing(1)

        vfxkitchen_banner_btn = QtWidgets.QPushButton()
        vfxkitchen_banner_btn.setFlat(True)
        vfxkitchen_banner_btn.setIconSize(QtCore.QSize(200,90))
        vfxkitchen_banner_btn.setMaximumHeight(15)
        vfxkitchen_banner_btn.setMaximumWidth(125)

        vfxkitchen_banner_btn.setIcon(QtGui.QIcon("ui/ui.data"))
        vfxkitchen_banner_btn.clicked.connect(self.open_vfxkitchen_website)

        self.min_btn = WindowTitleButton(self)
        self.min_btn.clicked.connect(self.minimize_pressed)

        self.max_btn = WindowTitleButton(self)
        self.max_btn.clicked.connect(self.maximize_pressed)

        self.x_btn = WindowTitleButton(self)
        self.x_btn.clicked.connect(self.close_pressed)

        self.layout().addWidget(vfxkitchen_banner_btn)
        self.layout().insertStretch(2, 1000)
        self.layout().addWidget(self.min_btn)
        self.layout().addWidget(self.max_btn)
        self.layout().addWidget(self.x_btn)

        self.counter = 1
        self.close_timer = QtCore.QTimer()
        self.close_timer.timeout.connect(self.fader)


    def fader(self):

        self.counter -= 0.01
        
        if self.counter < 0.1:
            self.close_timer.stop()
            self._parent.close()

        self._parent.setWindowOpacity(self.counter)

    def mouseDoubleClickEvent(self, event):

        self.maximize_pressed()

    def minimize_pressed(self):

        self._parent.setWindowState(QtCore.Qt.WindowMinimized)
        
    def maximize_pressed(self):

        if not self.maximized:
            self.maximized = True
            self._parent.setWindowState(QtCore.Qt.WindowMaximized)

        else:
            self.maximized = False
            self._parent.setWindowState(QtCore.Qt.WindowNoState)

    def close_pressed(self):
        
        self.close_timer.start(3)

    def open_vfxkitchen_website(self):
        
        webbrowser.open('https://www.vfxkitchen.net/')

    def mousePressEvent(self, event):

        self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):

        delta = QtCore.QPoint(event.globalPos() - self.old_pos)
        self._parent.move(self._parent.x() + delta.x(), self._parent.y() + delta.y())
        self.old_pos = event.globalPos()
