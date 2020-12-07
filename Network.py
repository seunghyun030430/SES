import json
import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import math

inf = math.inf

#json 데이터 편집
class Network():

    def __init__(self, filePath, name):

        with open(str(filePath), encoding="UTF-8") as jf:
            jd = json.load(jf)

            self.networkName = name

            #노드 데이터 가져오기
            self.n_number =  len(jd['elements']['nodes'])
            self.n_id = [jd['elements']['nodes'][i]['data']['id'] for i in range(self.n_number)]
            self.n_name = [jd['elements']['nodes'][i]['data']['name'] for i in range(self.n_number)]
            self.n_position = [(jd['elements']['nodes'][i]['position']['x'],jd['elements']['nodes'][i]['position']['y']) for i in range(self.n_number)]


            #엣지 데이터 가져오기
            self.e_number = len(jd['elements']['edges'])
            self.e_id = [jd['elements']['edges'][i]['data']['id'] for i in range(self.e_number)]
            self.e_source = [jd['elements']['edges'][i]['data']['source'] for i in range(self.e_number)]
            self.e_target = [jd['elements']['edges'][i]['data']['target'] for i in range(self.e_number)]
            self.e_weight = [jd['elements']['edges'][i]['data']['W'] for i in range(self.e_number)]
            self.e_st = [(self.e_source[i], self.e_target[i]) for i in range(self.e_number)]
            self.e_ts = [(self.e_target[i], self.e_source[i]) for i in range(self.e_number)]


            # Pandas 데이터 프레임 구축하기
            self.nodeDataFrame = pd.DataFrame({'Name':self.n_name,'Position':self.n_position},index=self.n_id)
            self.edgeDataFrame = pd.DataFrame({'Source':self.e_source, 'Target':self.e_target, 'ST':self.e_st , 'Weight':self.e_weight},index=self.e_id)


            #networkx Graph
            self.G = nx.Graph()
            self.G.add_nodes_from(self.nodeDataFrame.index)
            for i in range(self.e_number):
                self.G.add_edge(self.e_source[i], self.e_target[i], weight=self.e_weight[i])
            self.degree = nx.degree(self.G)


    def getDijkstra_pathEdge(self, source, targetlist, siteBoolList):
        n = int(max(self.edgeDataFrame.index))
        pathNodes = []
        pathEdges = []
        pathEdgeCosts = []
        self.changeSiteWeight(source, targetlist, siteBoolList)
        for ex in targetlist:
            pathNodes.append(nx.dijkstra_path(self.G, source, ex, weight='weight'))
            for pathNode in pathNodes:
                pathEdge = []
                pathEdgeCost = []
                for i in range(len(pathNode)-1):
                    pathEdge.append(str(self.getEdgeIndex(int(pathNode[i]),int(pathNode[i+1]))))
                    pathEdgeCost.append(self.getEdgeWeight(int(pathNode[i]),int(pathNode[i+1])))
            
            pathEdges.append(pathEdge)
            pathEdgeCosts.append(pathEdgeCost)
        exitNodes = [pathNodes[i][-1] for i in range(len(pathNodes))]

        return pathEdges, pathEdgeCosts, exitNodes


    def getMinCostPath(self, source, targetlist, siteBoolList):
        pathEdges, pathEdgesCosts, exitNode= self.getDijkstra_pathEdge(source, targetlist,siteBoolList)
        cost_numList = []

        for pathEdgeCost in pathEdgesCosts:
                cost_numList.append(sum(pathEdgeCost))

        min_index = cost_numList.index(min(cost_numList))
        
        return pathEdges[min_index], pathEdgesCosts[min_index], str(exitNode[min_index])


    def changeSiteWeight(self, source, targetlist, siteBoolList):
        changedWeight = []
        siteList = []
        for i in range(len(siteBoolList)):
            if siteBoolList[i] == True:
                siteList.append(self.n_id[i])

        for i in range(self.e_number):
            if (self.e_source[i] in siteList) or (self.e_target[i] in siteList):
                changedWeight.append(self.e_weight[i]+100)
            else:
                changedWeight.append(self.e_weight[i])

        self.edgeDataFrame = pd.DataFrame({'Source':self.e_source, 'Target':self.e_target, 'ST':self.e_st , 'Weight':changedWeight},index=self.e_id)

        self.G = nx.Graph()
        self.G.add_nodes_from(self.nodeDataFrame.index)
        for i in range(self.e_number):
            self.G.add_edge(self.e_source[i], self.e_target[i], weight=changedWeight[i])
        self.degree = nx.degree(self.G)


            
    def getEdgeIndex(self,source, target):
        n = int(max(self.edgeDataFrame.index))
        node_indexes = self.n_id
        conlen = np.full((n+1,n+1),inf)
        conedge_indexes = np.full((n+1,n+1), 0)

        for i in node_indexes:
            i = int(i)
            conlen[i,i] = 0

            #i와 연결된 edge의 index들의 list
            con_s = list(map(int,self.edgeDataFrame.index[(self.edgeDataFrame['Source'] == str(i))])) #i가 Source
            con_t = list(map(int,self.edgeDataFrame.index[(self.edgeDataFrame['Target'] == str(i))])) #i가 Target 
                
            #i와 연결된 node의 직접거리 수정
            for j in con_s:
                t = int(self.edgeDataFrame.loc[str(j),'Target'])
                w = int(self.edgeDataFrame.loc[str(j),'Weight'])
                conlen[i,t] = w
                conlen[t,i] = w
                conedge_indexes[i,t] = j
                conedge_indexes[t,i] = j

            for j in con_t:
                s = int(self.edgeDataFrame.loc[str(j),'Source'])
                w = int(self.edgeDataFrame.loc[str(j),'Weight'])
                conlen[i,s] = w
                conlen[s,i] = w
                conedge_indexes[i,s] = j
                conedge_indexes[s,i] = j

        return conedge_indexes[source, target]


    def getEdgeWeight(self,source,target):
        n = int(max(self.edgeDataFrame.index))
        node_indexes = self.n_id
        conlen = np.full((n+1,n+1),inf)
        conedge_indexes = np.full((n+1,n+1), 0)

        for i in node_indexes:
            i = int(i)
            conlen[i,i] = 0

            #i와 연결된 edge의 index들의 list
            con_s = list(map(int,self.edgeDataFrame.index[(self.edgeDataFrame['Source'] == str(i))])) #i가 Source
            con_t = list(map(int,self.edgeDataFrame.index[(self.edgeDataFrame['Target'] == str(i))])) #i가 Target 
                
            #i와 연결된 node의 직접거리 수정
            for j in con_s:
                t = int(self.edgeDataFrame.loc[str(j),'Target'])
                w = int(self.edgeDataFrame.loc[str(j),'Weight'])
                conlen[i,t] = w
                conlen[t,i] = w
                conedge_indexes[i,t] = j
                conedge_indexes[t,i] = j

            for j in con_t:
                s = int(self.edgeDataFrame.loc[str(j),'Source'])
                w = int(self.edgeDataFrame.loc[str(j),'Weight'])
                conlen[i,s] = w
                conlen[s,i] = w
                conedge_indexes[i,s] = j
                conedge_indexes[s,i] = j

        return conlen[source,target]

