# -*- coding: utf-8 -*-

"""
Created on Mon Dec 22 2:05:28 2014

@author: Ehsan
"""
#node fields
POS     = 0
STATUS  = 1
PARENT  = 2
G_COST  = 3
F_COST  = 4
#node status
ST_UNCHECKED = 0
ST_PENDING   = 1
ST_CHECKED   = 2
#neighbour fields
NB_ID = 0
NB_W  = 1

#def node(pos):
#    #pos[0,1], state[2], Parent[3], gCost[4], fCost[5]
#    return [pos, 0, None, 0, 0]

class Graph():
    size = 0
    vertex = []
    adjacent = []
#    idx = 0
    def __init__(self, filename):
        self.__loadFile(filename)
           
#    def __parse_adj(self,line):
#        line = line.split()
#        column = []
#        for i in range(int(line[0])):
#            column.append((int(line[1+ i*2]), float(line[1+ i*2+1])))
#        self.adjacent.append(column)
#        
#    def __parse_vert(self, line):
#        self.vertex.append(node(map(int,map(float, line.split()))))
        
    def __loadFile(self, filename):  
        with open(filename) as f:
#            self.vertex = []
            self.adjacent = []
            #helper functions to avoid the '.'             
            read = f.readline
            split = str.split            
            appendA = self.adjacent.append
#            appendV = self.vertex.append
            
            #size of the graph
            self.size = int(split(read())[0])
            
#            map(self.__parse_vert, f.readlines(self.size))
            SIZE = self.size
#            for i in xrange(self.size):
##                appendV([map(int,map(float, split(read()))), 0, None, 0, 0])
#                appendV(node(map(int,map(float, split(read())))))
            #complex but faster statement
            self.vertex = [[map(int,map(float, split(read()))), 0, None, 0, 0]
                            for i in xrange(SIZE)]    
            #adjacency list
#            map(self.__parse_adj, f.readlines(self.size))
                               
#            appendC = column.append
            for i in xrange(self.size):
#                line = f.readline().split()
                line = split(read())
                #line size  = int(line[0])
                column = [(int(line[1+ i*2]), float(line[1+ i*2+1]))
                                for i in xrange(int(line[0]))]
#                for i in xrange(int(line[0])):
#                    appendC((int(line[1+ i*2]), float(line[1+ i*2+1])))
                appendA(column)
#g = Graph("path/path.data")