# -*- coding: utf-8 -*-
"""
Created on Tue Dec 23 19:03:18 2014

@author: Ehsan
"""
def minify(filename, dic):
    with open(filename,"r") as old_file:    
        with open(filename[:-3] + "_fastify.py","w") as new_file:    
            for line in old_file:
                for (k,v) in dic.iteritems():
                    line = line.replace(k, v)
                new_file.write(line)

d = {"G.POS":"0", "G.STATUS":"1", "G.PARENT":"2", "G.G_COST":"3", "G.F_COST":"4", 
     "G.ST_UNCHECKED":"0", "G.ST_PENDING":"1", "G.ST_CHECKED":"2",
     "G.NB_ID":"0", "G.NB_W":"1"}
minify("pathfinder.py", d)                
                
                