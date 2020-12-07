from PyQt5.QtWidgets import *
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys
import matplotlib.pyplot as plt
import networkx as nx
import random

def main():
    Application = QApplication(sys.argv)
    w = QMainWindow()

    figure = matplotlib.figure.Figure(dpi=150)
    canvas = FigureCanvas(figure)
    figure.clf()
    ax1 = figure.add_subplot(1,1,1)
    G = nx.gnp_random_graph(10,0.3)
    for u,v,d in G.edges(data=True):
        d['weight'] = random.random()

    edges,weights = zip(*nx.get_edge_attributes(G,'weight').items())
    matplotlib.figure.Figure(dpi=150)

    pos = nx.spring_layout(G)
    nx.draw(G, pos, node_color='r', edgelist=edges, edge_color=weights, width=10.0, edge_cmap=plt.cm.Blues, ax=ax1)
    canvas.draw_idle()
    w.setCentralWidget(canvas)
    w.show()
    sys.exit(Application.exec_())

if __name__ == "__main__":
    main()