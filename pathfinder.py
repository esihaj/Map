# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 4:54:34 2014

@author: Ehsan
"""
import closestpoint
import graph as G
import heapq #probably should implement my own
from timeit import time
        
class PathPlanner():
    graph = None
    start = None
    end   = None
    search_list = []    
    def __init__(self, graph):
        self.graph = graph
        print len(self.graph.vertex)
        
    #TODO 
    #add other heuristic methods
    def heuristic(self, node):
#        return closestpoint.euclid_dist(node[G.POS], self.graph.vertex[self.end][G.POS])
        return closestpoint.manhattan_dist(node[G.POS], self.graph.vertex[self.end][G.POS])

    def __g_cost(self, child, parent, edge_weight):
        return edge_weight + self.graph.vertex[parent][G.COST]

    def __f_cost(self, child, parent, edge_weight):
        return self.__g_cost(child,parent,edge_weight) +  self.heuristic(self.graph.vertex[child])


    def __init_start(self):
        self.graph.vertex[self.start][G.STATUS] = G.ST_PENDING
        self.graph.vertex[self.start][G.COST] = 0
        self.graph.vertex[self.start][G.PARENT] = None
        for v in xrange(len(self.graph.vertex)):
            self.graph.vertex[v][G.STATUS] = G.ST_UNCHECKED

    def __add_child(self, child, parent, edge_weight):
#        print "adding %d -> %d (%d)" % (parent, child, edge_weight)
        self.graph.vertex[child][G.STATUS] = G.ST_PENDING
        self.graph.vertex[child][G.PARENT] = parent
        self.graph.vertex[child][G.COST] = self.__g_cost(child,parent,edge_weight)
        heapq.heappush(self.search_list, [self.__f_cost(child,parent,edge_weight), child]);
    def __relax_child(self, child, parent, edge_weight):
        self.graph.vertex[child][G.PARENT] = parent
        self.graph.vertex[child][G.COST] = self.__g_cost(child,parent,edge_weight)
        
    def __reverse(self,list):
        return list[::-1]
        
    def backtrace(self):
        curr = self.end
#        print "cur, ", curr
        path = [curr]
        while self.graph.vertex[curr][G.PARENT] != None:
            curr = self.graph.vertex[curr][G.PARENT]
            path.append(curr)
        return self.__reverse(path) 
    def T(self):
        return time.time() - self.start_time
        
    def Atime(self, start_node, end_node):
        self.start_time = time.time()
        self.Astar(start_node,end_node)
        print "total time = ", self.T()
        print "a total step of", self.step
        
    def Astar(self, start_node, end_node):
        self.start = start_node
        self.end = end_node        
        self.search_list = []
        heapq.heappush(self.search_list, [0,start_node])
        
        self.__init_start()
        print "init done", self.T()
        self.step = 0
        while self.search_list:
#            print "@step : ", step, "searchlist size = ", len(self.search_list)
#            print "list ["
#            for i in self.search_list :
#                print i, ","
#            print "]"
            self.step += 1            
            curr = heapq.heappop(self.search_list)
            self.graph.vertex[curr[1]][G.STATUS] = G.ST_CHECKED
            
            if curr[1] == self.end:#found the shortest path! :D
#                print "bingo!" 
                return self.backtrace()
                
            need_to_heapify = False
            t2 = time.time()
            for nb in self.graph.adjacent[curr[1]]:
                if self.graph.vertex[nb[G.NB_ID]][G.STATUS] == G.ST_UNCHECKED:
                    self.__add_child(nb[G.NB_ID], curr[1], nb[G.NB_W])
                    
                elif self.graph.vertex[nb[G.NB_ID]][G.STATUS] == G.ST_PENDING:
                    for p in xrange(len(self.search_list)):#find nb in the search list
                        #and check if the new way is shorter
                        if self.search_list[p][1] == nb[G.NB_ID]:
#                            print "relaxing", p.id
                            if self.__f_cost(nb[G.NB_ID], curr[1], nb[G.NB_W]) <self.search_list[p][0]:
#                                print "relaxed"
                                self.__relax_child(nb[G.NB_ID], curr[1], nb[G.NB_W])
                                self.search_list[p][0] = self.__f_cost(nb[G.NB_ID], curr[1], nb[G.NB_W])
                                need_to_heapify = True
                            break
            if time.time() - t2 > 0.0011:
                print "inner loop",time.time() - t2
            if need_to_heapify:
                t3 = time.time()
                heapq.heapify(self.search_list)
                if time.time() - t3 > 0.005:
                    print "heapify time", time.time() - t3
        
        return None #couldn't find any path 

t0 = time.time()
city_graph = G.Graph("path/path.data")
print "graph cunstruction time = ", time.time() - t0
p = PathPlanner(city_graph)
print "done"
print "*"*10
print "Astar"
p.Atime(0,100)
#print p.Astar(0,2)
#print "*"*10
#print p.Astar(1,2)
#print "*"*10
#print p.Astar(0,1)