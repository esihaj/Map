# -*- coding: utf-8 -*-
"""
Created on Tue Dec 23 17:02:24 2014

@author: Ehsan
"""

class some:
    lst = []
    def zfill(self):
       self.lst = [0 for x in range(10)]
    def get(self, id):
        return self.lst[id]
    def work(self):
        m = self.lst
        for i in range(10):
            m[i] = i
    def __str__(self):
        return str(self.lst)

s = some()
s.zfill()
print s
s.work()
print s
print "s actually changes"