# -*- coding: utf-8 -*-
"""
Created on Sun Dec 21 23:17:47 2014

@author: Ehsan
"""
from math import sqrt

def manhattan(point_list, start, cutoff = None):
    end = [0,0]
    min_dist = 10**7
    for i in point_list:
        if abs(i[0] - start[0])  + abs(i[1]- start[1]) < min_dist : 
            end = [i[0], i[1]]
            min_dist = abs(i[0] - start[0])  + abs(i[1]- start[1])
            if cutoff:
                if min_dist < cutoff: break
    return end
    
def euclidean(point_list, start, cutoff = None):
    end = [0,0]
    min_dist = 10**13
    for i in point_list:
       if (i[0]- start[0])**2 + (i[1]   - start[1])**2 < min_dist :
            end = [i[0], i[1]]
            min_dist = (i[0]- start[0])**2 + (i[1]   - start[1])**2
            if cutoff:
                if min_dist < cutoff: break
    return end

def eculid_dist(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)