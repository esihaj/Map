# -*- coding: utf-8 -*-
"""
Created on Sun Dec 21 23:17:47 2014

@author: Ehsan
"""
from math import sqrt


def euclid_dist2(p1, p2):
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2
    
def euclid_dist(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    
def manhattan_dist(p1, p2):
    return abs(p1[0] - p2[0])  + abs(p1[1]- p2[1])

def manhattan(point_list, start, cutoff = None):
    min_dist = 10**7
    index = None
    for i in xrange(len(point_list)):
        if manhattan_dist(point_list[i][0], start) < min_dist : 
            index = i
            min_dist = manhattan_dist(point_list[i][0], start)
            if cutoff:
                if min_dist < cutoff: break
    return index
    
def euclidean(point_list, start, cutoff = None):
    min_dist = 10**13
    index = None
    for i in xrange(len(point_list)):
       if euclid_dist2(point_list[i][0],start) < min_dist :
            index = i
            min_dist = euclid_dist2(point_list[i][0],start)
            if cutoff:
                if min_dist < cutoff: break
    return index
