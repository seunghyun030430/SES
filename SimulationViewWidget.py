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

class SimulationViewWidget(QWidget):
        
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle("Simulation View")
        self.resize(400,400)

        self.figure = matplotlib.figure.Figure(dpi=150)
        self.canvas = FigureCanvas(self.figure)
        
        self.layout = QGridLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)
        self.show()


    def updateView(self, selectedNetwork):
        self.drawGraph(selectedNetwork)


    def drawGraph(self,selectedNetwork):
        self.figure.clf()
        ax1 = self.figure.add_subplot(1,1,1)

        N = selectedNetwork
        nodePosition = N.nodeDataFrame["Position"]
        nodeLabels = N.nodeDataFrame['Name']
        nx.draw(N.G,nodePosition, labels=nodeLabels, node_size=[120+v[1]*50 for v in N.degree], font_family=font_name, with_labels=True,font_size=6,font_weight="bold", ax=ax1)
        self.canvas.draw_idle()


    def drawGraph_color(self, selectedNetwork, siteList, peopleList, pathList):
        self.figure.clf()
        ax1 = self.figure.add_subplot(1,1,1)
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
                    nodeColor.append('#DC143C')
                else:
                    nodeColor.append('#0000CD')
            elif peopleList[i] != 0:
                nodeColor.append('#0000CD')
            else:
                nodeColor.append('#C0C0C0')

        nodePosition = N.nodeDataFrame["Position"]
        nodeLabels = N.nodeDataFrame['Name']
        nx.draw(N.G,nodePosition, labels=nodeLabels, node_color=nodeColor, edge_color=edgeColor, node_size=[120+v[1]*50 for v in N.degree], font_family=font_name, with_labels=True, font_size=6, font_weight="bold", ax=ax1, width=edgeWidth, cmap=plt.cm.Reds)
        self.canvas.draw_idle()
