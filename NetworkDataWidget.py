from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class NetworkDataWidget(QTabWidget):

    def __init__(self):
        super().__init__()
        self.initUi()
        
        self.selectedNetwork = 0


    def initUi(self):
        self.setWindowTitle("Network Data")
        self.resize(400,400)

        self.nodeTable = QTableWidget()
        self.edgeTable = QTableWidget()

        self.addTab(self.nodeTable, "Nodes")
        self.addTab(self.edgeTable, "Edges")

        self.nodeTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.edgeTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    def setNodeTable(self):
        dataFrame = self.selectedNetwork.nodeDataFrame
        self.nodeTable.setColumnCount(len(dataFrame.columns))
        self.nodeTable.setRowCount(len(dataFrame.index))
        for i in range(len(dataFrame.index)):
            for j in range(len(dataFrame.columns)):
                self.nodeTable.setItem(i,j,QTableWidgetItem(str(dataFrame.iloc[i,j])))


    def setEdgeTable(self):
        dataFrame = self.selectedNetwork.edgeDataFrame
        self.edgeTable.setColumnCount(len(dataFrame.columns))
        self.edgeTable.setRowCount(len(dataFrame.index))
        for i in range(len(dataFrame.index)):
            for j in range(len(dataFrame.columns)):
                self.edgeTable.setItem(i,j,QTableWidgetItem(str(dataFrame.iloc[i,j])))

    def updateData(self, selectedNetwork):
        self.selectedNetwork = selectedNetwork
        self.setNodeTable()
        self.setEdgeTable()