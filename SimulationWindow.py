from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from SimulationSettingWidget import SimulationSettingWidget
from SimulationViewWidget import SimulationViewWidget
from NetworkListWidget import NetworkListWidget
from ResultWindow import ResultWindow


class SimulationWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUi()
        self.networkList = []
        self.networkSiteSettingList = []   
        self.networkPeopleSettingList = []
        self.networkExitList = [['291','290'],
                                ['426', '292','313','305'],
                                ['302','292','313','305','379'],
                                ['302','292','470','313','305']]
        self.networkExitLinkList = [{},
                                    {'426':'280', '292':'292', '313':'313', '305':'305'},
                                    {'302':'426','313':'313','292':'292','305':'305','379':'428'},
                                    {'302':'302','292':'292','313':'313','470':'379','305':'305'}] #연결된 아래층 탈출 노드
        self.selectedNetwork = 0
        

    def initUi(self):
        self.setWindowTitle("Simulator")
        self.resize(1400,800)

        self.simulationSettingWidget = SimulationSettingWidget()
        self.simulationViewWidget = SimulationViewWidget()
        self.networkListWidget = NetworkListWidget()
        self.resultWindow = ResultWindow()
        self.setCentralWidget(self.simulationViewWidget)

        self.dockWidgetRight = QDockWidget("Simulation Setting")
        self.dockWidgetLeft = QDockWidget("Network List")
        self.dockWidgetRight.setAllowedAreas(Qt.RightDockWidgetArea)
        self.dockWidgetLeft.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.dockWidgetRight.setWidget(self.simulationSettingWidget)
        self.dockWidgetLeft.setWidget(self.networkListWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockWidgetRight)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidgetLeft)

        #Event Manager
        self.networkListWidget.networkChangedSignal.connect(self.setSelectedNetwork)
        self.simulationSettingWidget.siteSettingUpdatedSignal.connect(self.saveSiteSetting)
        self.simulationSettingWidget.peopleSettingUpdatedSignal.connect(self.savePeopleSetting)
        self.simulationSettingWidget.runSimulationSignal.connect(self.runSimulation)


    def setSelectedNetwork(self,selectedNetwork):
        if self.selectedNetwork != 0:
            self.simulationSettingWidget.saveSetting()
        self.selectedNetwork = selectedNetwork
        index = self.networkList.index(self.selectedNetwork)
        self.updateGraphColor()
        self.simulationSettingWidget.updateTableSetSite(self.selectedNetwork, self.networkSiteSettingList[index])
        self.simulationSettingWidget.updateTableAllocatePeople(self.selectedNetwork, self.networkPeopleSettingList[index])
        

    def updateNetworkList(self):
        self.networkListWidget.updateList(self.networkList)
        if self.networkSiteSettingList == []:
            self.networkPeopleSettingList = [[0 for j in range(self.networkList[j].n_number)] for j in range(len(self.networkList))]
            self.networkSiteSettingList = [[False for j in range(self.networkList[j].n_number)] for j in range(len(self.networkList))]
        

    def saveSiteSetting(self, siteList):
        index = self.networkList.index(self.selectedNetwork)
        self.networkSiteSettingList[index] = siteList
        if index<(len(self.networkList)-1):
            for i in range(self.networkList[index].n_number):
                if self.networkSiteSettingList[index][i]:
                    if self.networkList[index].n_id[i] in self.networkExitList[index]:
                        ReverseDic = {v:k for k,v in self.networkExitLinkList[index+1].items()}
                        print(self.networkList[index].n_id[i], ReverseDic)
                        uplinkExit = ReverseDic[(self.networkList[index].n_id[i])]
                        self.networkSiteSettingList[index+1][self.networkList[index+1].n_id.index(uplinkExit)] = True
                     # 각 층에서 도착지점 아래쪽 노드의 탈출경로가 재난 발생 지역인지 확인 후 그 위쪽 노드 재난 발생으로 설정
        self.updateGraphColor()


    def savePeopleSetting(self, peopleList):
        index = self.networkList.index(self.selectedNetwork)
        self.networkPeopleSettingList[index] = peopleList
        self.updateGraphColor()


    def updateGraphColor(self):
        index = self.networkList.index(self.selectedNetwork)
        self.simulationViewWidget.drawGraph_color(self.selectedNetwork, self.networkSiteSettingList[index], self.networkPeopleSettingList[index], [])


    def runSimulation(self):
        N = len(self.networkList)
        totalResult = []
        #{nodeIndex, peopleNumber, VerticalPathList, VerticalCostList, VerticalExitList}


        for verticalIndex in range(N):

            result = []
            for i in range(self.networkList[verticalIndex].n_number):

                verticalPathList = [[]for i in range(N)]
                verticalCostList = [[]for i in range(N)]
                verticalExitList = [""for i in range(N)]
                
                if (self.networkPeopleSettingList[verticalIndex][i] != 0):
                    network = self.networkList[verticalIndex]
                    startNodeName = network.n_id[i]
                    nodeName = network.n_id[i]

                    for j in range(verticalIndex, -1 ,-1):
                        network = self.networkList[j]
                        pathList, costList, exitNode = network.getMinCostPath(nodeName,self.networkExitList[j], self.networkSiteSettingList[j])
                        print(pathList, costList, exitNode)
                        downLink = self.networkExitLinkList[j].get(exitNode)
                        nodeName = downLink
                        verticalPathList[j]=pathList
                        verticalCostList[j]=costList
                        verticalExitList[j]=exitNode

                    result.append([startNodeName, self.networkPeopleSettingList[verticalIndex][i], verticalPathList, verticalCostList, verticalExitList])
            
            totalResult.append(result)

        self.resultWindow.networkList = self.networkList
        self.resultWindow.update(self.networkList, self.networkSiteSettingList, self.networkPeopleSettingList, totalResult)
        self.resultWindow.show()


            

                    

            
