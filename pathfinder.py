# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 4:54:34 2014

@author: Ehsan
"""
#import closestpoint
import heapq #probably should implement my own
import graph as G

    
class PathPlanner():
    graph = None
    start = None
    end   = None
    search_list = []    
    def __init__(self, filename):  
        self.graph = G.Graph(filename)
        print len(self.graph.vertex)
        
        
    #TODO 
    #add other heuristic methods

#    def manhattan_dist(p1, p2):
#        return abs(p1[0] - p2[0])  + abs(p1[1]- p2[1])
#    def m_dist(self, node1):
#        return abs(node1[G.POS][0] - self.graph.vertex[self.end][G.POS][0])  + abs(node1[G.POS][1]- self.graph.vertex[self.end][G.POS][1])
    def heuristic(self, node):
##        return closestpoint.euclid_dist(node[G.POS], self.graph.vertex[self.end][G.POS])
        return 100*(abs(node[G.POS][0] - self.graph.vertex[self.end][G.POS][0])  + abs(node[G.POS][1]- self.graph.vertex[self.end][G.POS][1]))

#    def __g_cost(self, child, parent, edge_weight):
#        return edge_weight + self.graph.vertex[parent][G.G_COST]
#
#    def __f_cost(self, child, parent, edge_weight):
#        return self.__g_cost(child,parent,edge_weight) +  self.heuristic(self.graph.vertex[child])


    def __init_start(self):
        v = self.graph.vertex[self.start]
        v[G.G_COST] = 0
        v[G.F_COST] = self.heuristic(v)#?
        v[G.PARENT] = None
        heapq.heappush(self.search_list, [self.heuristic(v),self.start])

#    def __add_child(self, child, parent, edge_weight):
##        print "adding %d -> %d (%d)" % (parent, child, edge_weight)
#        self.graph.vertex[child][G.STATUS] = G.ST_PENDING
#        self.graph.vertex[child][G.PARENT] = parent
#        self.graph.vertex[child][G.G_COST] = self.__g_cost(child,parent,edge_weight)
#        self.graph.vertex[child][G.F_COST] = self.__f_cost(child,parent,edge_weight)
#        heapq.heappush(self.search_list, [self.__f_cost(child,parent,edge_weight), child]);
#    
#    def __relax_child(self, search_id, child, parent, edge_weight):
#        if self.__f_cost(child, parent, edge_weight) < self.search_list[search_id][0]:        
#            self.graph.vertex[child][G.PARENT] = parent
#            self.graph.vertex[child][G.G_COST] = self.__g_cost(child,parent,edge_weight)
#            self.graph.vertex[child][G.F_COST] = self.search_list[search_id][0] = self.__f_cost(child,parent,edge_weight)
#            return True
#        return False
        
    def __reverse(self,list):
        return list[::-1]
        
    def backtrace(self):
        path_len = 0
        v= self.graph.vertex
        a = self.graph.adjacent
        curr = self.end
#        print "cur, ", curr
        path = [curr]
        while self.graph.vertex[curr][G.PARENT] != None:
            curr = v[curr][G.PARENT]
            for nb in a[curr]:
                if nb[G.NB_ID] == path[-1]:
                    path_len += nb[G.NB_W]
                    break
            path.append(curr)
        return (path_len, self.__reverse(path))

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
            state[curr[1]] = G.ST_CHECKED
            
            if curr[1] == end_node:#found the shortest path! :D
                return self.backtrace()
                
            need_to_heapify = False
            for nb in adjc[curr[1]]:
                if state[nb[G.NB_ID]] == G.ST_UNCHECKED:#add it as a child
#                    self.__add_child(nb[G.NB_ID], curr[1], nb[G.NB_W])
                    child = v[nb[G.NB_ID]]
                    state[nb[G.NB_ID]] = G.ST_PENDING
                    child[G.PARENT] = curr[1]
                    child[G.G_COST] = nb[G.NB_W] + v[curr[1]][G.G_COST]# G = edge weight + G(parent)
                    child[G.F_COST] = child[G.G_COST] + H(child) # F = G + H 
                    heapq.heappush(heap, [child[G.F_COST], nb[G.NB_ID]]);
                    
                elif state[nb[G.NB_ID]] == G.ST_PENDING:  #Try to relax it
#                    self.__relax_child(self.search_list.index( [v[nb[G.NB_ID]][G.F_COST],nb[G.NB_ID]] ),
#                                       nb[G.NB_ID], curr[1], nb[G.NB_W])
                    child = v[nb[G.NB_ID]]                    
                    search_id = heap.index( [child[G.F_COST],nb[G.NB_ID]] )
                    
                    #new Costs
                    new_g_cost = nb[G.NB_W] + v[curr[1]][G.G_COST]# G = edge weight + G(parent)                    
                    new_f_cost = new_g_cost + H(child) # F = G + H 
                    
                    #if better ...
                    if new_f_cost < heap[search_id][0]:#relax it   
                        child[G.PARENT] = curr[1]
                        child[G.G_COST] = new_g_cost
                        child[G.F_COST] = heap[search_id][0] = new_f_cost
                        need_to_heapify = True
                    

            if need_to_heapify:
                heapq.heapify(heap)
        
        return (-1,None) #couldn't find any path 

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