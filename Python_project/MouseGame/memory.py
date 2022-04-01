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
        if self.currentNode is None or len(self.currentNode.childs)<10:
            return randint(0,5)
        else:
            max=-1000000;
            actionMax=-1;
            for i in range(len(self.currentNode.childs)):
                if(self.currentNode.childs[i].value>max):
                    max=self.currentNode.childs[i].value
                    actionMax= self.currentNode.childs[i].action
            return actionMax