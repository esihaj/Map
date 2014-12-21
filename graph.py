# -*- coding: utf-8 -*-

"""
Created on Mon Dec 22 2:05:28 2014

@author: Ehsan
"""

class Graph():
    size = 0
    vertex = []
    adjacent = []
    def loadFile(self, filename):    
        with open(filename) as f:
            #size of the graph
            self.size = int(f.readline().split()[0])
            #list of vertecies
            for i in range(self.size):
                self.vertex.append(map(float, f.readline().split()))
            #adjacency list
            for i in range(self.size):
                line = f.readline().split()
                #line size  = int(line[0])
                column = []
                for i in range(int(line[0])):
                    column.append((int(line[1+ i*2]), float(line[1+ i*2+1])))
                self.adjacent.append(column)

            
    