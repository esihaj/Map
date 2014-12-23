# -*- coding: utf-8 -*-

"""
Created on Mon Dec 22 2:05:28 2014

@author: Ehsan
"""
#node fields
POS     = 0
STATUS  = 1
PARENT  = 2
COST    = 3
#node status
ST_UNCHECKED = 0
ST_PENDING   = 1
ST_CHECKED   = 2
#neighbour fields
NB_ID = 0
NB_W  = 1

def node(pos):
    #pos[0,1], state[2], Parent[3], gCost[4]
    return [pos, 0, None, 0]
    
class Graph():
    size = 0
    vertex = []
    adjacent = []
    def __init__(self, filename):
        self.__loadFile(filename)
        
    def __loadFile(self, filename):    
        with open(filename) as f:
            #size of the graph
            self.size = int(f.readline().split()[0])
            #list of vertecies
            for i in range(self.size):
                self.vertex.append(node(map(float, f.readline().split())))
            #adjacency list
            for i in range(self.size):
                line = f.readline().split()
                #line size  = int(line[0])
                column = []
                for i in range(int(line[0])):
                    column.append((int(line[1+ i*2]), float(line[1+ i*2+1])))
                self.adjacent.append(column)