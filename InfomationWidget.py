from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class InfomationWidget(QWidget):
        
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle("Infomation")
        self.resize(400,400)

        