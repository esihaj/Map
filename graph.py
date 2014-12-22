# -*- coding: utf-8 -*-

"""
Created on Mon Dec 22 2:05:28 2014

@author: Ehsan
"""
class NodeStatus():
    UNCHECKED = 0
    PENDING = 1
    CHECKED = 2

class Node():
    pos = [0,0]
    status = NodeStatus.UNCHECKED
    parent = None
    g_cost = 0.0
    def __init__(self, pos):
        self.pos = pos
        
class neighbour():
    id = 0
    weight = 0
    def __init__(self, index, w):
        self.id = index
        self.weight = w
def zero(pos):
    return pos + [0, None, 0]
    
class Graph():
    size = 0
    vertex = []
    adjacent = []
    def __init__(self, filename):
        self.loadFile(filename)
        
    def loadFile(self, filename):    
        with open(filename) as f:
            #size of the graph
            self.size = int(f.readline().split()[0])
            #list of vertecies
            for i in range(self.size):
                self.vertex.append(Node(map(float, f.readline().split())))
            #adjacency list
            for i in range(self.size):
                line = f.readline().split()
                #line size  = int(line[0])
                column = []
                for i in range(int(line[0])):
                    column.append((int(line[1+ i*2]), float(line[1+ i*2+1])))
                self.adjacent.append(column)

            
    