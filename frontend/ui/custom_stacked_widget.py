from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets

class CustomStackedWidget(QtWidgets.QWidget):

    def __init__(self, parent = None):
        super(CustomStackedWidget, self).__init__(parent)
        self._parent = parent

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(QtCore.Qt.AlignCenter)

        self.widgets = []
        self.current_widget_index = 0

        self.addWidget(QtWidgets.QWidget())

    def setCentralWidget(self, widget):
        
        self.widgets.append(widget)
        
        for w in self.widgets:
            w.hide()
        
        self.layout().addWidget(widget)
        widget.show()

    def count(self):

        return len(self.widgets)

    def addWidget(self, widget):
        
        self.widgets.append(widget)
        self.layout().addWidget(widget)
        self.showCurrentWidget()

        return self.count()-1

    def replaceWidget(self, idx, widget):
        
        self.widgets[idx].setParent(None)
        self.widgets[idx] = widget
        self.layout().addWidget(widget)
        self.showCurrentWidget()

    def currentWidget(self):

        return self.widgets[self.current_widget_index]

    def setCurrentIndex(self, index):

        if index <= self.count():
            self.current_widget_index = index
            self.showCurrentWidget()

    def showCurrentWidget(self):
        
        if (self.count() > 0):

            for widget in self.widgets:
                widget.hide()

            selected_widget = self.widgets[self.current_widget_index]
            selected_widget.show()