# -*- coding: utf-8 -*-
"""
Created on Sun Dec 21 23:17:47 2014

@author: Ehsan
"""
def manhattan(point_list, start):
    end = [0,0]
    min_dist = 10**7
    for i in point_list:
        if abs(i[0] - start[0])  + abs(i[1]- start[1]) < min_dist : 
            end = [i[0], i[1]]
            min_dist = abs(i[0] - start[0])  + abs(i[1]- start[1])
    return end
def euclidean(point_list, start):
    end = [0,0]
    min_dist = 10**13
    for i in point_list:
       if (i[0]- start[0])**2 + (i[1]   - start[1])**2 < min_dist :
            end = [i[0], i[1]]
            min_dist = (i[0]- start[0])**2 + (i[1]   - start[1])**2
    return end