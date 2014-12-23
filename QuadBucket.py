# -*- coding: utf-8 -*-
"""
Created on Wed Dec 24 02:13:56 2014

@author: Ehsan
"""
import closestpoint

class QBucket:
    'Data Structure Used to Find The proper files to display'
    size = 0
    capacity = 200
    filled = False
    child = [[None, None], [None, None]]
    bbox = [[0,0], [0,0]]
    bucket = []
    file_name = ''
    def __init__(self, bbox=None):
        self.child = [[None, None], [None, None]]
        self.size = 0
        self.filled = False
        self.bucket = []
        self.bbox = bbox if bbox else [[0,0], [0,0]]
        
    def add_node(self , index, pos):
        if not self.filled:
            self.bucket.append((index, pos))
            self.size += 1
            if self.size > self.capacity:
                self.break_down()
                self.filled = True
        else: 
            self.size += 1
            self.push_to_child(index,pos)
        
    def push_to_child(self, index, pos):
        for i in range(2):
            for j in range(2):
                if self.child[i][j].bbox[0][0]<pos[0] < self.child[i][j].bbox[1][0] and  self.child[i][j].bbox[0][1]<pos[1] < self.child[i][j].bbox[1][1]:
                    self.child[i][j].add_node(index,pos)
                    
    def break_down(self):
        bbox = self.bbox        
        midx = (bbox[0][0] + bbox[1][0])/2.0
        midy = (bbox[0][1] + bbox[1][1])/2.0        
        self.child[0][0] = QBucket([[bbox[0][0], bbox[0][1]],[midx,midy]])        
        self.child[0][1] = QBucket([[bbox[0][0], midy],[midx,bbox[1][1]]])        
        self.child[1][0] = QBucket([[midx, bbox[0][1]],[bbox[1][0],midy]])        
        self.child[1][1] = QBucket([[midx, midy],[bbox[1][0],bbox[1][1]]])
        
        for p in self.bucket:
            for i in range(2):
                for j in range(2):
                    if self.child[i][j].bbox[0][0]<p[1][0] < self.child[i][j].bbox[1][0] and  self.child[i][j].bbox[0][1]<p[1][1] < self.child[i][j].bbox[1][1]:
                        self.child[i][j].add_node(p[0], p[1])
        self.bucket = []
        
    def find_closest(self,pos):
        Min = 10**6
        Min_id = -1                
        if self.bbox[0][0]<pos[0] < self.bbox[1][0] and  self.bbox[0][1]<pos[1] < self.bbox[1][1]:
            
            if self.filled:
                  for i in range(2):
                    for j in range(2):
                        (val,idx) = self.child[i][j].find_closest(pos)
                        if val < Min:
                            Min = val
                            Min_id = idx
            
            else: 
                for i in self.bucket:
                    if closestpoint.manhattan_dist(pos, i[1]) < Min:
                        Min = closestpoint.manhattan_dist(pos, i[1])
                        Min_id = i[0]
        return (Min, Min_id)
        
    def intersect(self, b_1, b_2):
        # courtesy of 'http://stackoverflow.com/questions/16005136/how-do-i-see-if-two-rectangles-intersect-in-javascript-or-pseudocode'
        aLeftOfB = b_1[1][0] < b_2[0][0]
        aRightOfB = b_1[0][0] > b_2[1][0]
        aAboveB = b_1[0][1] > b_2[1][1]
        aBelowB = b_1[1][1] < b_2[0][1]
        return  not (aLeftOfB or aRightOfB or aAboveB or aBelowB)