from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PyQt5 import uic

form_class = uic.loadUiType("SimulationSettingWidget.ui")[0]

class SimulationSettingWidget(QWidget, form_class):

    siteSettingUpdatedSignal = pyqtSignal(list)
    peopleSettingUpdatedSignal = pyqtSignal(list)
    runSimulationSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUi()

        self.settingsPeople = []
        self.settingsSite = []


    def initUi(self):
        self.setWindowTitle("Simulation Setting")
        self.TableSetSite.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.TableAllocatePeople.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        #ComboBox
        self.comboBoxType.addItem("지진")
        self.comboBoxType.addItem("화재")
        self.comboBoxLevel.addItem("위험")
        self.comboBoxLevel.addItem("보통")
        self.comboBoxLevel.addItem("약함")

        self.runButton.clicked.connect(self.runSimulation)

    def updateTableSetSite(self, Network, setting):
        self.selectedNetwork = Network
        dataFrame = self.selectedNetwork.nodeDataFrame
        self.TableSetSite.setColumnCount(len(dataFrame.columns))
        self.TableSetSite.setRowCount(len(dataFrame.index))
        for i in range(len(dataFrame.index)):
            self.TableSetSite.setItem(i,0,QTableWidgetItem(str(dataFrame.iloc[i,0])))
        
        self.checkBoxList = []
        for i in range(len(dataFrame.index)):
            ckbox = QCheckBox()
            self.checkBoxList.append(ckbox)

        for i in range(len(dataFrame.index)):
            cellWidget = QWidget()
            layoutCB = QHBoxLayout(cellWidget)
            layoutCB.addWidget(self.checkBoxList[i])
            self.checkBoxList[i].stateChanged.connect(self.saveSiteSetting)
            if type(setting) is list:
                if setting[i]:
                    self.checkBoxList[i].toggle()
            layoutCB.setAlignment(Qt.AlignCenter)
            layoutCB.setContentsMargins(0,0,0,0)
            cellWidget.setLayout(layoutCB)

            self.TableSetSite.setCellWidget(i,1,cellWidget)


    def updateTableAllocatePeople(self, Network, setting):
        self.selectedNetwork = Network
        dataFrame = self.selectedNetwork.nodeDataFrame
        self.TableAllocatePeople.setColumnCount(len(dataFrame.columns))
        self.TableAllocatePeople.setRowCount(len(dataFrame.index))
        for i in range(len(dataFrame.index)):
            self.TableAllocatePeople.setItem(i,0,QTableWidgetItem(str(dataFrame.iloc[i,0])))
        
        self.spinBoxList = []
        for i in range(len(dataFrame.index)):
            sbox = QSpinBox()
            self.spinBoxList.append(sbox)

        for i in range(len(dataFrame.index)):
            cellWidget = QWidget()
            layoutS = QHBoxLayout(cellWidget)
            layoutS.addWidget(self.spinBoxList[i])
            self.spinBoxList[i].valueChanged.connect(self.savePeopleSetting)
            if type(setting) is list:
                self.spinBoxList[i].setValue(setting[i])
            layoutS.setAlignment(Qt.AlignCenter)
            layoutS.setContentsMargins(0,0,0,0)
            cellWidget.setLayout(layoutS)

            self.TableAllocatePeople.setCellWidget(i,1,cellWidget)


    def saveSiteSetting(self):
        self.settingsSite = []
        for cb in self.checkBoxList:
            self.settingsSite.append(cb.isChecked())
        self.siteSettingUpdatedSignal.emit(self.settingsSite)

    
    def savePeopleSetting(self):
        self.settingsPeople = []
        for sb in self.spinBoxList:
            self.settingsPeople.append(sb.value())
        self.peopleSettingUpdatedSignal.emit(self.settingsPeople)


    def saveSetting(self):
        self.savePeopleSetting()
        self.saveSiteSetting()


    def runSimulation(self):
        self.saveSetting()
        self.runSimulationSignal.emit()