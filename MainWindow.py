from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

#Import Widgets
from Network import Network
from PreferenceWidget import PreferenceWidget
from NetworkViewWidget import NetworkViewWidget
from InfomationWidget import InfomationWidget
from NetworkLoaderWidget import NetworkLoaderWidget
from NetworkListWidget import NetworkListWidget
from NetworkDataWidget import NetworkDataWidget
from SimulationWindow import SimulationWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):

        #General Setting
        self.setWindowTitle("SEJONG EVACUATION SYSTEM v1.0")
        self.resize(1500,800)
        self.networkList = []
        self.selectedNetwork = 0


        #Widget Setting
        self.preferenceWidget = PreferenceWidget()
        self.infomationWidget = InfomationWidget()
        self.networkViewWidget = NetworkViewWidget()
        self.networkLoaderWidget = NetworkLoaderWidget()
        self.networkListWidget = NetworkListWidget()
        self.networkDataWidget = NetworkDataWidget()
        self.simulationWindow = SimulationWindow()

        self.setCentralWidget(self.networkViewWidget)

        #Menu Setting
        self.menuBar = self.menuBar()

        #StateBar Setting
        self.statusBar().showMessage("HELLO")

        #File
        fileMenu = self.menuBar.addMenu("File")
        file_ExitAction = QAction("Exit", self)
        file_ExitAction.triggered.connect(qApp.quit)
        fileMenu.addAction(file_ExitAction)

        #Setting
        settingMenu = self.menuBar.addMenu("Setting")
        setting_PreferenceAction = QAction("Preference",self)
        setting_PreferenceAction.triggered.connect(self.openPreference)
        settingMenu.addAction(setting_PreferenceAction)

        #Network
        networkMenu = self.menuBar.addMenu("Network")
        networkLoadAction = QAction("Load Network", self)
        networkLoadAction.triggered.connect(self.openLoadNetwork)
        networkMenu.addAction(networkLoadAction)

        #Simulation
        simulationMenu = self.menuBar.addMenu("Simulation")
        simulationAction = QAction("Open Simulator", self)
        simulationAction.triggered.connect(self.openSimulator)
        simulationMenu.addAction(simulationAction)

        #Help
        helpMenu = self.menuBar.addMenu("Help")
        help_InfoAction = QAction("Info", self)
        help_InfoAction.triggered.connect(self.openInfo)
        helpMenu.addAction(help_InfoAction)

        #DockWidget
        self.dockWidgetLeft = QDockWidget("Network List", self)
        self.dockWidgetRight = QDockWidget("Network Data", self)
        self.dockWidgetLeft.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.dockWidgetRight.setAllowedAreas(Qt.RightDockWidgetArea)
        self.dockWidgetLeft.setWidget(self.networkListWidget)
        self.dockWidgetRight.setWidget(self.networkDataWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidgetLeft)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockWidgetRight)

        #Event Manager
        self.networkLoaderWidget.appendNewNetworkSignal.connect(self.appendNetwork)
        self.networkListWidget.networkChangedSignal.connect(self.setSelectedNetwork)

        #File upload
        self.networkList.append(Network('C:/Users/SeungHyun/Desktop/SES/H_1.cyjs', "H1"))
        self.networkList.append(Network('C:/Users/SeungHyun/Desktop/SES/H_2.cyjs', "H2"))
        self.networkList.append(Network('C:/Users/SeungHyun/Desktop/SES/H_3.cyjs', "H3"))
        self.networkList.append(Network('C:/Users/SeungHyun/Desktop/SES/H_4.cyjs', "H4"))
        self.updateNetworkList()
        self.openSimulator()

    def openPreference(self):
        self.preferenceWidget.show()

    def openInfo(self):
        self.infomationWidget.show()

    def openLoadNetwork(self):
        self.networkLoaderWidget.show()

    def openSimulator(self):
        self.simulationWindow.networkList = self.networkList
        self.simulationWindow.updateNetworkList()
        self.simulationWindow.show()
    
    def appendNetwork(self, network):
        self.networkList.append(network)
        self.updateNetworkList()


    def setSelectedNetwork(self,selectedNetwork):
        self.selectedNetwork = selectedNetwork
        self.networkViewWidget.updateView(self.selectedNetwork)
        self.networkDataWidget.updateData(self.selectedNetwork)


    def updateNetworkList(self):
        self.networkListWidget.updateList(self.networkList)
