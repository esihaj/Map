# -*- coding: utf-8 -*-
"""
Created on Tue Dec 23 20:02:06 2014

@author: Ehsan
"""
import matplotlib.pyplot as plt

class Hist():
    size = 0
    raw = []
    def __init__(self, filename):
        self.__loadFile(filename)
        
    def __plot(self, bigger):
        new_data = [i for i in self.raw if i >= bigger]
        print "Node Degree Histogram >=" + str(bigger), len(new_data)
        plt.hist(new_data)
        plt.title("Node Degree Histogram >=" + str(bigger))
        plt.xlabel("Value")
        plt.ylabel("Frequency")
        plt.show()
        
    def __loadFile(self, filename):  
        with open(filename) as f:
            #helper functions to avoid the '.'             
            read = f.readline
            split = str.split            
            
            #size of the graph
            SIZE = self.size = int(split(read())[0])
            
            vertex = [[map(int,map(float, split(read()))), 0, None, 0, 0]
                            for i in xrange(SIZE)]    
            #adjacency list
            self.raw = [int(split(read())[0]) for i in xrange(SIZE)]
    def plot(self, cutoffs):
        for i in cutoffs:            
            self.__plot(i)
    def count_zero(self):
        c = 0
        for i in self.raw:
            if not i: c +=1
        return c   
                
h = Hist("../path/path.data")
print "zeros", h.count_zero()
h.plot([0,4,8,10,13,15,20,25, 30])