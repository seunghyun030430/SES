from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import matplotlib
import matplotlib.font_manager as fm
fm.get_fontconfig_fonts()
font_location = 'C:/Windows/Fonts/MALGUNSL.ttf' # For Windows
font_name = fm.FontProperties(fname=font_location).get_name()
matplotlib.rc('font', family=font_name)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import networkx as nx

class NetworkViewWidget(QWidget):
        
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle("Network View")
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
        nx.draw(N.G,nodePosition, labels=nodeLabels, node_size=[120+v[1]*50 for v in N.degree], node_color="#C0C0C0", font_family=font_name, with_labels=True,font_size=6,font_weight="bold", ax=ax1)
        self.canvas.draw_idle()
