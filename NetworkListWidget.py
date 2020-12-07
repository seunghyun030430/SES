from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class NetworkListWidget(QListView):
    
    networkChangedSignal = pyqtSignal("PyQt_PyObject")

    def __init__(self):
        super().__init__()
        self.initUi()
        self.networkList = []


    def initUi(self):
        self.setWindowTitle("Infomation")
        self.resize(300,300)
        self.model = QStandardItemModel()
        self.setModel(self.model)

        self.clicked.connect(self.networkSelected)


    def networkSelected(self, index):
        i = int(index.row())
        self.selectedNetwork = self.networkList[i]
        self.networkChangedSignal.emit(self.selectedNetwork)


    def updateList(self, networkList):
        self.model.clear()
        self.networkList = networkList
        for network in networkList:
            self.model.appendRow(QStandardItem(network.networkName))

