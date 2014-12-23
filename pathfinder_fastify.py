# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 4:54:34 2014

@author: Ehsan
"""
#import closestpoint
import heapq #probably should implement my own
from math import sqrt

    
class PathPlanner():
    graph = None
    start = None
    end   = None
    search_list = []    
    def __init__(self, filename):  
        import graph as G
        self.graph = G.Graph(filename)
        print len(self.graph.vertex)
        
        
    #TODO 
    #add other heuristic methods

#    def manhattan_dist(p1, p2):
#        return abs(p1[0] - p2[0])  + abs(p1[1]- p2[1])
#    def m_dist(self, node1):
#        return abs(node1[0][0] - self.graph.vertex[self.end][0][0])  + abs(node1[0][1]- self.graph.vertex[self.end][0][1])
    def heuristic(self, node):
#        return sqrt((node[0][0] - self.graph.vertex[self.end][0][0]) ** 2 + (node[0][1]- self.graph.vertex[self.end][0][1]) ** 2)
#        return 0
        return abs(node[0][0] - self.graph.vertex[self.end][0][0])  + abs(node[0][1]- self.graph.vertex[self.end][0][1])

#    def __g_cost(self, child, parent, edge_weight):
#        return edge_weight + self.graph.vertex[parent][3]
#
#    def __f_cost(self, child, parent, edge_weight):
#        return self.__g_cost(child,parent,edge_weight) +  self.heuristic(self.graph.vertex[child])


    def __init_start(self):
        v = self.graph.vertex[self.start]
        v[3] = 0
        v[4] = self.heuristic(v)#?
        v[2] = None
        heapq.heappush(self.search_list, [self.heuristic(v),self.start])

#    def __add_child(self, child, parent, edge_weight):
##        print "adding %d -> %d (%d)" % (parent, child, edge_weight)
#        self.graph.vertex[child][1] = 1
#        self.graph.vertex[child][2] = parent
#        self.graph.vertex[child][3] = self.__g_cost(child,parent,edge_weight)
#        self.graph.vertex[child][4] = self.__f_cost(child,parent,edge_weight)
#        heapq.heappush(self.search_list, [self.__f_cost(child,parent,edge_weight), child]);
#    
#    def __relax_child(self, search_id, child, parent, edge_weight):
#        if self.__f_cost(child, parent, edge_weight) < self.search_list[search_id][0]:        
#            self.graph.vertex[child][2] = parent
#            self.graph.vertex[child][3] = self.__g_cost(child,parent,edge_weight)
#            self.graph.vertex[child][4] = self.search_list[search_id][0] = self.__f_cost(child,parent,edge_weight)
#            return True
#        return False
        
    def __reverse(self,list):
        return list[::-1]
        
    def backtrace(self):
        curr = self.end
#        print "cur, ", curr
        path = [curr]
        while self.graph.vertex[curr][2] != None:
            curr = self.graph.vertex[curr][2]
            path.append(curr)
        return self.__reverse(path) 

    def Astar(self, start_node, end_node):
        self.start = start_node
        self.end = end_node    
        v = self.graph.vertex
        adjc = self.graph.adjacent
        state = [0] * self.graph.size
        heap = self.search_list = []  
        H = self.heuristic
        self.__init_start()

        while heap:
            curr = heapq.heappop(heap)
            state[curr[1]] = 2
            
            if curr[1] == end_node:#found the shortest path! :D
                return self.backtrace()
                
            need_to_heapify = False
            for nb in adjc[curr[1]]:
                if state[nb[0]] == 0:#add it as a child
#                    self.__add_child(nb[0], curr[1], nb[1])
                    child = v[nb[0]]
                    state[nb[0]] = 1
                    child[2] = curr[1]
                    child[3] = nb[1] + v[curr[1]][3]# G = edge weight + G(parent)
                    child[4] = child[3] + H(child) # F = G + H 
                    heapq.heappush(heap, [child[4], nb[0]]);
                    
                elif state[nb[0]] == 1:  #Try to relax it
#                    self.__relax_child(self.search_list.index( [v[nb[0]][4],nb[0]] ),
#                                       nb[0], curr[1], nb[1])
                    child = v[nb[0]]                    
                    search_id = heap.index( [child[4],nb[0]] )
                    
                    #new Costs
                    new_g_cost = nb[1] + v[curr[1]][3]# G = edge weight + G(parent)                    
                    new_f_cost = new_g_cost + H(child) # F = G + H 
                    
                    #if better ...
                    if new_f_cost < heap[search_id][0]:#relax it   
                        child[2] = curr[1]
                        child[3] = new_g_cost
                        child[4] = heap[search_id][0] = new_f_cost
                        need_to_heapify = True
                    

            if need_to_heapify:
                heapq.heapify(heap)
        
        return None #couldn't find any path 

#t0 = time.time()
p = PathPlanner("path/path.data")
#print "graph cunstruction time = ", time.time() - t0

print "done"
print "*"*10
print "Astar"
#p.Atime(0,100)

#print p.Astar(0,2)
#print "*"*10
#print p.Astar(1,2)
#print "*"*10
#print p.Astar(0,1)