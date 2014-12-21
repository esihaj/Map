# -*- coding: utf-8 -*-
"""
Created on Sun Dec 21 22:48:30 2014

@author: Ehsan
"""

import timeit
import math
import random as rnd

x = []
Max = 500000
Max_coord = 10**6
for i in range(Max):
    x.append((rnd.randint(0,Max_coord), rnd.randint(0,Max_coord)));

def dist(x,y):
    return math.sqrt(x**2 + y**2)
    
def find_closest_m(node_list, start):
    end = [0,0]
    min_dist = 10**7
    for i in node_list:
        #manhattan distance    
        if abs(i[0] - start[0])  + abs(i[1]- start[1]) < min_dist : 
            end = [i[0], i[1]]
            min_dist = abs(i[0] - start[0])  + abs(i[1]- start[1])
    print end
    #print min_dist
def find_closest_e(node_list, start):
    min_dist = 10**13
    end = [0,0]
    for i in node_list:
        #elucidian distance    
        if (i[0]- start[0])**2 + (i[1]   - start[1])**2 < min_dist :
            end = [i[0], i[1]]
            min_dist = (i[0]- start[0])**2 + (i[1]   - start[1])**2
    print end

def find_closest_e_sqrt(node_list, start):
    end = [0,0]
    min_dist = 10**8
    for i in node_list:
        #sqrt(elucidian) distance    
        if math.sqrt((i[0]- start[0])**2 + (i[1]   - start[1])**2) < min_dist : 
           end = [i[0], i[1]]           
           min_dist = math.sqrt((i[0]- start[0])**2 + (i[1]   - start[1])**2)
    print end
    
def test():
    print "hi"
test()
sample_point = (rnd.randint(0,Max_coord), rnd.randint(0,Max_coord));