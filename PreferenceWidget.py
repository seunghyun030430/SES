from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class PreferenceWidget(QWidget):
        
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle("Preference")
        self.resize(400,400)

        