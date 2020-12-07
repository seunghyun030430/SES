from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Network import Network
import json
import pandas as pd

class NetworkLoaderWidget(QWidget):

    appendNewNetworkSignal = pyqtSignal("PyQt_PyObject")

    def __init__(self):
        super().__init__()
        self.initUi()
        self.newNetworkName = ""

    def initUi(self):
        self.setWindowTitle("Network Loader")
        self.resize(400,400)

        #File Open
        self.openFileButton = QPushButton("File open")
        self.openFileButton.clicked.connect(self.openNetworkFile)
        self.fileLabel = QLabel()

        self.okButton = QPushButton("OK")
        self.okButton.clicked.connect(self.loadNetwork)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.close)

        #File Name Line Edit
        self.NetworkNameEdit = QLineEdit(self)
        self.NetworkNameEdit.textChanged[str].connect(self.onChanged)
        #Layout
        self.verticalLayout = QVBoxLayout()
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.addWidget(self.openFileButton)
        self.horizontalLayout.addWidget(self.fileLabel)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout.addWidget(self.okButton)
        self.verticalLayout.addWidget(self.cancelButton)
        self.verticalLayout.addWidget(self.NetworkNameEdit)

        self.setLayout(self.horizontalLayout)

    
    def openNetworkFile(self):
        fileName = QFileDialog.getOpenFileName(self)
        self.fileLabel.setText(fileName[0])

    def loadNetwork(self):
        if self.newNetworkName == "":
            pass
        else:
            newNetwork = Network(self.fileLabel.text(),self.newNetworkName)
            self.appendNewNetworkSignal.emit(newNetwork)
            self.close()

    def onChanged(self, text):
        self.newNetworkName = text
        self.NetworkNameEdit.adjustSize()
