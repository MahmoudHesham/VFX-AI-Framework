import sys
import json
import os
import importlib
import subprocess
import configparser
import requests

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from qtmodern.styles import dark

from ui.custom_stacked_widget import CustomStackedWidget
from ui.custom_titlebar_widget import WindowTitleBar

BUTTONS_STYLESHEET = "QPushButton:hover{background-color:orangered}\
                      QPushButton{background-color:#ffa500; color:black; border: 0px;}"

class MainWin(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MainWin, self).__init__(parent=parent)
        self.configurations = {}
        self.current_config = None

        self.init_ui()
        self.check_for_settings()

    def sizeHint(self):

        return QtCore.QSize(1280, 720)

    def check_for_settings(self):

        settings_file = "settings.ini"
        
        if not os.path.exists(settings_file):
            return
            
        settings = configparser.ConfigParser()
        settings.read(settings_file)

        if settings.has_section("autoload"):
            for k, v in settings.items('autoload'):
                config_file = os.path.abspath(v)
                self.load_configuration(config_file)

    def init_ui(self):

        self.setLayout(QtWidgets.QVBoxLayout())
        self.setWindowTitle("Workspace")
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(10, 5, 10, 10)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint)

        self.titlebar = WindowTitleBar(self)
        self.layout().addWidget(self.titlebar)

        solutions_gb = QtWidgets.QGroupBox("Configurations")
        solutions_gb.setLayout(QtWidgets.QVBoxLayout())
        solutions_gb.layout().setContentsMargins(0, 0, 0, 0)
        
        self.solutions_list = QtWidgets.QListWidget()
        self.solutions_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.solutions_list.customContextMenuRequested.connect(self.solutions_context_menu)
        self.solutions_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.switch_btn = QtWidgets.QPushButton("Switch")
        self.switch_btn.clicked.connect(self.config_switched_fn)
        self.switch_btn.setStyleSheet(BUTTONS_STYLESHEET)
        self.switch_btn.setMinimumHeight(20)

        solutions_gb.layout().addWidget(self.solutions_list)
        solutions_gb.layout().addWidget(self.switch_btn)

        self.stack_widget = CustomStackedWidget(self)

        stacked_widget_gb = QtWidgets.QGroupBox("Interface")
        stacked_widget_gb.setLayout(QtWidgets.QVBoxLayout())
        stacked_widget_gb.layout().setContentsMargins(0, 0, 0, 0)

        self.empty_widget = QtWidgets.QWidget()

        self.server_url = QtWidgets.QLineEdit()
        self.server_url.setPlaceholderText("Server URL")
        self.server_url.setEnabled(False)

        self.config_logo_banner = QtWidgets.QLabel()
        self.config_logo_banner.setAlignment(QtCore.Qt.AlignCenter)
        self.config_logo_banner.setHidden(True)

        self.submit_btn = QtWidgets.QPushButton("Submit")
        self.submit_btn.clicked.connect(self.submit_server_request)
        self.submit_btn.setStyleSheet(BUTTONS_STYLESHEET)
        self.submit_btn.setMinimumHeight(20)
        self.submit_btn.setHidden(True)

        stacked_widget_gb.layout().addWidget(self.server_url)
        stacked_widget_gb.layout().addWidget(self.config_logo_banner, 0, QtCore.Qt.AlignTop)
        stacked_widget_gb.layout().addWidget(self.stack_widget)
        stacked_widget_gb.layout().addWidget(self.submit_btn)

        self.outputs_widget = QtWidgets.QGroupBox("Outputs")
        self.outputs_widget.setLayout(QtWidgets.QVBoxLayout())
        self.outputs_widget.layout().setContentsMargins(0, 0, 0, 0)
        
        self.filesystem_model = QtWidgets.QFileSystemModel()
        self.empty_model = QtWidgets.QFileSystemModel()

        self.outputs_tree = QtWidgets.QTreeView()
        self.outputs_tree.setRootIsDecorated(False)
        self.outputs_tree.setColumnWidth(0, 150)
        self.outputs_tree.setModel(self.filesystem_model)
        self.outputs_tree.doubleClicked.connect(self.output_file_clicked_fn)

        self.outputs_widget.layout().addWidget(self.outputs_tree)

        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(solutions_gb)
        splitter.addWidget(stacked_widget_gb)
        splitter.addWidget(self.outputs_widget)
        splitter.setSizes([80, 220, 120])

        self.layout().addWidget(splitter)

        self.status_bar = QtWidgets.QLabel()
        self.status_bar.setMaximumHeight(20)
        
        footer_layout = QtWidgets.QHBoxLayout()
        footer_layout.addWidget(self.status_bar)
        footer_layout.addWidget(QtWidgets.QSizeGrip(self), 0,  QtCore.Qt.AlignRight)
        self.layout().addLayout(footer_layout)

    def submit_server_request(self):

        selected_config = self.configurations[self.current_config]
        
        config_url = selected_config['url']
        config_widget = selected_config['widget']
        request_body = config_widget.request_body
        output_directory = os.path.abspath(selected_config['output'])

        try:
            config_request = requests.post(config_url, json=request_body)
            self.status_bar.setText('Request successed! response object will be save in the output directory.')

            response = config_request.json()
            config_widget.recived_data_handler(response=response, output=output_directory)
        
        except requests.exceptions.ConnectionError as e:
            limited_error_msg = " ".join(str(e).split(" ")[:15])
            self.status_bar.setText(limited_error_msg)

    def output_file_clicked_fn(self, item_index):
        
        selected_filepath = item_index.model().filePath(item_index)

        if os.path.isdir(selected_filepath):
        	return

        if sys.platform == 'linux':
            subprocess.Popen([f'gio open {selected_filepath}'], shell=True)
        
        else:
            subprocess.Popen([selected_filepath], shell=True)

    def solutions_context_menu(self, position):

        menu = QtWidgets.QMenu()

        switch_solution = menu.addAction("Switch")
        switch_solution.setVisible(False)
        switch_solution.triggered.connect(self.config_switched_fn)

        menu.addSeparator()

        import_solution_cfg = menu.addAction("Import solution configuration...")
        import_solution_cfg.triggered.connect(self.import_solution_fn)

        remove_solution_cfg = menu.addAction("Remove solution")
        remove_solution_cfg.setVisible(False)
        remove_solution_cfg.triggered.connect(lambda:self.remove_solution_fn(selected_item=selected_items[0]))

        selected_items = self.sender().selectedItems()
        if(selected_items):
            switch_solution.setVisible(True)
            remove_solution_cfg.setVisible(True)
           
        menu.exec_(self.sender().viewport().mapToGlobal(position))

    def import_solution_fn(self):

        config_files, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Select solution configuration", None, "VK Configuration (*.vk)")
        
        for config in config_files:
            if(config.endswith(".vk")):
                self.load_configuration(config)

    def remove_solution_fn(self, selected_item):

        config_name = selected_item.text()
        selected_config = self.configurations[config_name]

        # replacing config widget with an empty one to maintain loaded configurations indices, might change in the future.
        self.stack_widget.replaceWidget(selected_config['widget_index'], self.empty_widget)

        self.configurations.pop(config_name, None)
        self.solutions_list.takeItem(self.solutions_list.row(selected_item))

        if(self.current_config == config_name):
            self.clear_interface()
            self.current_config = None

    def config_switched_fn(self):

        selected_items = self.solutions_list.selectedItems()

        if not selected_items:
            self.clear_interface()
            return

        self.current_config = selected_items[0].text()
        selected_config = self.configurations[self.current_config]
        widget_index = selected_config["widget_index"]
        banner_filepath = f"plugins/data/{selected_config['banner']}"

        self.submit_btn.setHidden(False)
        self.outputs_tree.setModel(self.filesystem_model)
        self.stack_widget.setCurrentIndex(widget_index)
        self.filesystem_model.setRootPath(selected_config['output'])
        self.outputs_tree.setRootIndex(self.filesystem_model.index(selected_config['output']))
        self.server_url.setText(selected_config['url'])
        self.status_bar.setText(f"Selected configuration: {self.current_config}")
        self.config_logo_banner.setPixmap(QtGui.QPixmap(banner_filepath))
        self.config_logo_banner.setHidden(False)

    def load_configuration(self, config_filepath):

        if not os.path.exists(config_filepath):
            print("Config file doesn't exists.")
            return

        with open(config_filepath) as f:
            config_data = json.load(f)

        if (config_data['name'] in self.configurations):
            print("Configuration already loaded.")
            return

        self.solutions_list.addItem(config_data["name"])

        spec = importlib.util.spec_from_file_location(config_data['plugin'], f"plugins/{config_data['plugin']}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        configuration_widget = module.Register(self)

        config_output = f"output/{config_data['plugin'][:-3]}"
        if not (os.path.exists(config_output)):
            os.mkdir(config_output)
        
        widget_index = self.stack_widget.addWidget(configuration_widget)
        self.configurations[config_data["name"]] = {'widget': configuration_widget, 'plugin': config_data['plugin'], 'output': config_output,
        'widget_index': widget_index, 'url': config_data['url'], 'banner': config_data['banner']}

    def clear_interface(self):

        self.outputs_tree.setModel(self.empty_model)
        self.stack_widget.setCurrentIndex(0)
        self.submit_btn.setHidden(True)
        self.config_logo_banner.setHidden(True)
        self.server_url.clear()

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    dark(app)

    main_win = MainWin()
    main_win.show()
    
    sys.exit(app.exec_())