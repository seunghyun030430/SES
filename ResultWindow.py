from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
fm.get_fontconfig_fonts()
font_location = 'C:/Windows/Fonts/MALGUNSL.ttf' # For Windows
font_name = fm.FontProperties(fname=font_location).get_name()
matplotlib.rc('font', family=font_name)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import networkx as nx

class ResultWindow(QMainWindow):
        
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle("Simulation Result")
        self.resize(1800,900)

        self.figure = matplotlib.figure.Figure()
        self.canvas = FigureCanvas(self.figure)
        self.nodeTable = QTableWidget()
        self.nodeTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.nodeTable.clicked.connect(self.nodeSelected)

        self.model = QStandardItemModel()
        self.networkListView = QListView()
        self.networkListView.setModel(self.model)
        self.networkListView.clicked.connect(self.networkSelected)

        #DockWidget
        self.dockWidgetLeft = QDockWidget("Network List", self)
        self.dockWidgetRight = QDockWidget("Target Node Tabel", self)
        self.dockWidgetLeft.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.dockWidgetRight.setAllowedAreas(Qt.RightDockWidgetArea)
        self.dockWidgetLeft.setWidget(self.networkListView)
        self.dockWidgetRight.setWidget(self.nodeTable)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidgetLeft)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockWidgetRight)

        self.setCentralWidget(self.canvas)

        self.networkList = []
        self.totalResult = []
        self.selectedNetwork = None
        self.selectedNetworkIndex = None
        self.selectedNodeIndex = None
        self.selectedNodeName = None

    def networkSelected(self, index):
        i = int(index.row())
        self.selectedNetwork = self.networkList[i]
        self.selectedNetworkIndex = i
        self.updateNodeSetting()


    def nodeSelected(self, item):
        i = int(item.row())
        self.selectedNodeResult = self.totalResult[self.selectedNetworkIndex]
        self.selectedNodeName = self.selectedNodeResult[i][0]
        self.selectedNodeIndex = i
        self.update(self.networkList, self.siteLists, self.peopleLists, self.totalResult)


    def updateNodeSetting(self):
        selectedResult = self.totalResult[self.selectedNetworkIndex]
        self.nodeTable.setColumnCount(5)
        self.nodeTable.setRowCount(len(selectedResult))
        for i in range(len(selectedResult)):
            for j in range(5):
                self.nodeTable.setItem(i,j, QTableWidgetItem(str(selectedResult[i][j])))
        


    def update(self, networkList, siteLists, peopleLists, totalResult):
        GraphList = []
        self.model.clear()
        self.figure.clf()
        self.siteLists = siteLists
        self.peopleLists = peopleLists
        self.totalResult = totalResult
        self.networkList = networkList
        print(self.totalResult)
        for i in range(len(self.networkList)):
            GraphList.append(self.figure.add_subplot(1, len(self.networkList) ,i+1))

        for network in self.networkList:
            self.model.appendRow(QStandardItem(network.networkName))

        if self.selectedNetworkIndex is None:
            for i in range(len(self.networkList)):
                network = self.networkList[i]
                self.drawGraph_color(network, siteLists[i], peopleLists[i], self.selectedNodeName, [], GraphList[i])
        else: 
            r = totalResult[self.selectedNetworkIndex]
            for i in range(len(self.networkList)):
                network = self.networkList[i]
                self.drawGraph_color(network, siteLists[i], peopleLists[i], self.selectedNodeName, r[self.selectedNodeIndex][2][i], GraphList[i])


    def drawGraph_color(self, selectedNetwork, siteList, peopleList, startNode, pathList, ax):
        N = selectedNetwork
        edgeColor = []
        edgeIndex = []
        edgeWidth = []
        for i in range(N.e_number):      
            if (list(N.G.edges)[i] in N.e_st):
                index = N.e_st.index(list(N.G.edges)[i])
            elif (list(N.G.edges)[i] in N.e_ts):
                index = N.e_ts.index(list(N.G.edges)[i])
            edgeIndex.append(N.e_id[index])
            edgeWidth.append(N.e_weight[index]*0.7+1) # adjust width

        for edge_id in edgeIndex:
            if edge_id in pathList:
                edgeColor.append('#00FF7F')
            else:
                edgeColor.append('#696969')

        nodeColor = []
        for i in range(len(siteList)):
            if siteList[i]:
                if peopleList[i] == 0:
                    if N.n_id[i] == startNode:
                        nodeColor.append('#CCCCCC')
                    else:
                        nodeColor.append('#DC143C')
                else:
                    nodeColor.append('#0000CD')
            elif peopleList[i] != 0:
                nodeColor.append('#0000CD')
            else:
                nodeColor.append('#C0C0C0')

        nodePosition = N.nodeDataFrame["Position"]
        nodeLabels = N.nodeDataFrame['Name']
        ax.set_title(N.networkName)
        nx.draw(N.G,nodePosition, labels=nodeLabels, node_color=nodeColor, edge_color=edgeColor, node_size=[80+v[1]*50 for v in N.degree], font_family=font_name, with_labels=True, font_size=5, font_weight="bold", ax=ax, width=edgeWidth, cmap=plt.cm.Reds)
        self.canvas.draw()

    
