from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow
import sys
from Network import Network
from SimulationWindow import SimulationWindow
def main():

    networkList = []
    networkList.append(Network('C:/Users/SeungHyun/Desktop/SES/H_1.cyjs', "H1"))
    networkList.append(Network('C:/Users/SeungHyun/Desktop/SES/H_2.cyjs', "H2"))
    networkList.append(Network('C:/Users/SeungHyun/Desktop/SES/H_3.cyjs', "H3"))
    networkList.append(Network('C:/Users/SeungHyun/Desktop/SES/H_4.cyjs', "H4"))
    Application = QApplication(sys.argv)
    w = SimulationWindow()
    w.networkList = networkList
    w.updateNetworkList()
    w.show()
    sys.exit(Application.exec_())

if __name__ == "__main__":
    main()
