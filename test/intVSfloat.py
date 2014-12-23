# -*- coding: utf-8 -*-
"""
Created on Tue Dec 23 15:06:47 2014

@author: Ehsan
"""
#result : xrange > range , int == float

SIZE = 1000000
def fl_r():
    for i in range(SIZE):
        a = 0.05 + 9.659
def fl_xr():
    for i in xrange(SIZE):
        a = 0.05 + 9.659
def int_r():
    for i in range(SIZE):
        a = 50 + 9659
def int_xr():
    for i in xrange(SIZE):
        a = 50 + 9659
#%timeit int_xr()
