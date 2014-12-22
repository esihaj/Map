# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 4:54:34 2014

@author: Ehsan
"""
import closestpoint
from graph import *
import heapq #probably should implement my own
class heapObj():
    id = 0
    val = 0
    
    def __init__(self, id, val):
        self.id = id
        self.val = val
        
    def __cmp__(self, other):
        return cmp(self.val, other.val)
    def __str__(self):
        return str(self.id)
        
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
#        return closestpoint.euclid_dist(node.pos, self.graph.vertex[self.end].pos)
        return closestpoint.manhattan_dist(node.pos, self.graph.vertex[self.end].pos)

    def __g_cost(self, child, parent, edge_weight):
        return edge_weight + self.graph.vertex[parent].g_cost

    def __f_cost(self, child, parent, edge_weight):
        return self.__g_cost(child,parent,edge_weight) +  self.heuristic(self.graph.vertex[child])


    def __init_start(self):
        self.graph.vertex[self.start].status = NodeStatus.PENDING
        self.graph.vertex[self.start].g_cost = 0.0
        self.graph.vertex[self.start].parent = None
        for v in xrange(len(self.graph.vertex)):
            self.graph.vertex[v].status = NodeStatus.UNCHECKED

    def __add_child(self, child, parent, edge_weight):
#        print "adding %d -> %d (%d)" % (parent, child, edge_weight)
        self.graph.vertex[child].status = NodeStatus.PENDING
        self.graph.vertex[child].parent = parent
        self.graph.vertex[child].g_cost = self.__g_cost(child,parent,edge_weight)
        heapq.heappush(self.search_list, heapObj(child, self.__f_cost(child,parent,edge_weight)))
    def __relax_child(self, child, parent, edge_weight):
        self.graph.vertex[child].parent = parent
        self.graph.vertex[child].g_cost = self.__g_cost(child,parent,edge_weight)
        
    def __reverse(self,list):
        return list[::-1]
        
    def backtrace(self):
        curr = self.end
#        print "cur, ", curr
        path = [curr]
        while self.graph.vertex[curr].parent != None:
            curr = self.graph.vertex[curr].parent
            path.append(curr)
        return self.__reverse(path) 
        
    def Astar(self, start_node, end_node):
        self.start = start_node
        self.end = end_node        
        self.search_list = []
        heapq.heappush(self.search_list, heapObj(start_node, 0))
        
        self.__init_start()
        step = 0
        while self.search_list:
#            print "@step : ", step, "searchlist size = ", len(self.search_list)
#            print "list ["
#            for i in self.search_list :
#                print i, ","
#            print "]"
            curr = heapq.heappop(self.search_list)
            self.graph.vertex[curr.id].status = NodeStatus.CHECKED
            
            if curr.id == self.end:#found the shortest path! :D
#                print "bingo!" 
                return self.backtrace()
                
            need_to_heapify = False
            
            for nb in self.graph.adjacent[curr.id]:
                if self.graph.vertex[nb[0]].status == NodeStatus.UNCHECKED:
                    self.__add_child(nb[0], curr.id, nb[1])
                    
#                elif self.graph.vertex[nb.id].status == NodeStatus.PENDING:
#                    for p in xrange(len(self.search_list)):#find nb in the search list
#                        #and check if the new way is shorter
#                        if self.search_list[p].id == nb.id:
##                            print "relaxing", p.id
#                            if self.__f_cost(nb.id, curr.id, nb.weight) <self.search_list[p].val:
##                                print "relaxed"
#                                self.__relax_child(nb.id, curr.id, nb.weight)
#                                self.search_list[p].val = self.__f_cost(nb.id, curr.id, nb.weight)
#                                need_to_heapify = True
#                            break

            if need_to_heapify:
#                print "heapify"
                heapq.heapify(self.search_list)
        
        return None #couldn't find any path 

#city_graph = Graph("path/path.data")
#p = PathPlanner(city_graph)
print "done"
print "*"*10
#print p.Astar(0,2)
#print "*"*10
#print p.Astar(1,2)
#print "*"*10
#print p.Astar(0,1)