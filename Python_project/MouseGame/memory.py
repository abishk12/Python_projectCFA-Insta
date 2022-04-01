from random import randint

actionNames= ["forward", "turnLeft", "turnRight", "touchFront", "touchLeft", "touchRight"]

class Node:
    def __init__(self, action, value):
        self.name= actionNames[action]+str(value)
        self.action=action
        self.value= value
        self.childs= []

    def addChild(self, node):
        self.childs.append(node)

    def isChild(self, node):
        for i in range(len(self.childs)):
            if self.childs[i].name==node.name:
                return True
        return False

class Memory:
    def __init__(self):
        self.nodes= []
        self.currentNode= None
        self.bestNode=None

    def size(self):
        size= len(self.nodes)
        for i in range(len(self.nodes)):
            size+= len(self.nodes[i].childs)
        return size

    def update(self, node):
        if self.bestNode is None or node.value > self.bestNode.value  :
            self.bestNode= node
        if self.currentNode is None:
            self.currentNode= node
        else:
            nodeIndex= self.getMemoryIndex(node)
            if nodeIndex==-1:
                self.nodes.append(node)
            else:
                node= self.nodes[nodeIndex]
            if not self.currentNode.isChild(node):
                self.currentNode.addChild(node)
            self.currentNode= node

    def getMemoryIndex(self, node):
        for i in range(len(self.nodes)):
            if self.nodes[i].name==node.name:
                return i
        return -1

    def chooseBestAction(self):
        if self.currentNode is None or len(self.currentNode.childs)<9:
            print("aleatoire")
            return randint(0,5)
        else:
            print("dijkstra")
            return self.dijkstra(self.currentNode)

    def initDijkstra(self, nodeDepart):
        self.tabDistance= [-1000000] * len(self.nodes)
        nodeIndex= self.getMemoryIndex(nodeDepart)
        self.tabDistance[nodeIndex]=0

    def searchBestNode(self, listNodesIndex):
        max= -1000000
        nodeMax= None
        for i in listNodesIndex:
            if self.tabDistance[i] > max:
                max= self.tabDistance[i]
                nodeMax= i
        return nodeMax
    
    def updateDistance(self, node1, node2):
        indexNode1= self.getMemoryIndex(node1)
        indexNode2= self.getMemoryIndex(node2)
        if self.tabDistance[indexNode2] < self.tabDistance[indexNode1] + node2.value:
            self.tabDistance[indexNode2]= self.tabDistance[indexNode1] + node2.value

    def dijkstra(self, nodeDepart):
        self.initDijkstra(nodeDepart)
        nodes=[]
        for i in range(len(self.nodes)):
            nodes.append(i)
        while len(nodes)>0 :
            index1= self.searchBestNode(nodes)
            nodes.remove(index1)
            s1= self.nodes[index1]
            for s2 in s1.childs:
                self.updateDistance(s1, s2)
        return self.nodes[self.getPath()].action
    
    def getPath(self):
        path= []
        max=-1000000
        for i in range(len(self.tabDistance)):
            if self.tabDistance[i] > max:
                path= []
                max= self.tabDistance[i]
                path.append(i)
            elif max == self.tabDistance[i]:
                path.append(i)
        return path[randint(0, len(path)-1)]