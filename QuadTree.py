# -*- coding: utf-8 -*-
"""
Created on Tue Dec 02 23:17:43 2014

@author: Ehsan
"""
import json
import os
import sys
import pygame
import graph
import closestpoint
import pathfinder

LOGLEVEL = 0
LOG_GENERAL = 1
LOG_INTERSECT = 1.3
LOG_TREE = 2
LOG_GENERATE = 3



def LOG(string, level = LOG_GENERAL): 
    if level <= LOGLEVEL: print string
        
class QTree:
    'Data Structure Used to Find The proper files to display'
    count = 0
    child = [[None, None], [None, None]]
    bbox = [[0,0], [0,0]]
    z_level = -1
    file_name = ''
    def __init__(self, zoom, file_name):
        self.z_level = zoom
        self.file_name = file_name
        self.child = [[None, None], [None, None]]
        self.bbox = [[0,0], [0,0]]
        self.load_bbox()
        QTree.count += 1
        
    def load_bbox(self):
        try:
            with open(self.file_name) as json_file:
                tmp_json = json.load(json_file)
                if 'bbox' not in tmp_json:
                    raise AttributeError('No Bounding Box Found In The' + self.file_name + ' file')
                b = tmp_json['bbox']
                self.bbox = [[b[0],b[1]], [b[2],b[3]]]
        except:
            print 'Can\'t Load/ Read bbox from "' + self.file_name +'"'
    
    def append_node(self , index_x, index_y, node):
        LOG("inserting into [%s][%s]" % (index_x, index_y), LOG_TREE)
        LOG("\t Z : p[%s] c[%s]" % (self.z_level, node.z_level), LOG_TREE)
        self.child[index_y][index_x] = node

    def intersect(self, b_1, b_2):
        # courtesy of 'http://stackoverflow.com/questions/16005136/how-do-i-see-if-two-rectangles-intersect-in-javascript-or-pseudocode'
        aLeftOfB = b_1[1][0] < b_2[0][0]
        aRightOfB = b_1[0][0] > b_2[1][0]
        aAboveB = b_1[0][1] > b_2[1][1]
        aBelowB = b_1[1][1] < b_2[0][1]
        return  not (aLeftOfB or aRightOfB or aAboveB or aBelowB)

    def find_area(self, zoom, view):
        if zoom < self.z_level: 
            LOG("None : zoom < self.z %s %s" % (zoom, self.z_level), LOG_INTERSECT)
            return None
        elif self.intersect(view, self.bbox):
            LOG("intersect @z %s | " % (self.z_level) + self.file_name, LOG_INTERSECT)
            LOG([[int(self.bbox[0][0]), int(self.bbox[0][1])], [int(self.bbox[1][0]),int(self.bbox[1][1])]], LOG_INTERSECT)
            #check if the children also intersect @zoom 
            res = []
            for i in range(2):
                for j in range(2):
                    if self.child[i][j] :
                        tmp = self.child[i][j].find_area(zoom, view)
                        if tmp is not None:
                            res.append(tmp)
            LOG("child intersect @z %s count : %s \n" % (self.z_level, len(res)), LOG_INTERSECT)
            if len(res) > 1 : #if the children returned anything just return it
                return res
            elif len(res) == 1:
                return res[0]
            else : return self.file_name # otherwise return self
        else: return None
            
        
#utility : isFile
base_dir = os.path.dirname(__file__) + '/'
def isFile(name): 
    #print "\tcheking ", base_dir + name, os.path.isfile(base_dir + name)    
    return os.path.isfile(base_dir + name)
def get_x(level_counter, x_old = 0) : return (1 if level_counter % 2 else 0) + x_old * 2
def get_y(level_counter, y_old = 0) : return (0 if level_counter < 2 else 1) + y_old * 2
    #assuming What Reza Keramti Told is True
def get_path(zoom, x, y) : return "json files/Level "+str(zoom)+"/" + "+00"+str(zoom)+",+00"+str(x)+",+00"+str(y)+".json"

def generate_Tree(parent_zoom, x_old, y_old, parent_node):
    debg = False if parent_zoom == 3 else True
    for L in range(4):
        y_new = get_y(L, y_old)
        x_new = get_x(L, x_old)
        file_new = get_path(parent_zoom+1, x_new, y_new)
#        print "%s @/ (%s,%s)" % (parent_zoom +1, x_new, y_new)
        if isFile(file_new):
            node_new = QTree(parent_zoom +1, file_new)
            generate_Tree(parent_zoom +1, x_new, y_new, node_new)
            parent_node.append_node(get_x(L), get_y(L), node_new)
        elif debg : LOG("CAN'T find File detail File @ Z: %s, y: %s, x: %s" % (parent_zoom + 1, y_new, x_new), LOG_GENERATE)
    LOG("\n", LOG_GENERATE)

def explore(node, l = 0):
    for y in range(2):
        for x in range(2):
            if node.child[y][x] is not None:
                #print '\t'*l + '[%s][%s] @ Z %s' % (y, x, node.child[y][x].z_level) + '[FILE]', node.child[y][x].file_name                
                print '\t'*l + '[%s][%s] @ Z %s' % (y, x, node.child[y][x].z_level) + 'B', node.child[y][x].bbox
                explore(node.child[y][x], l+1)
            elif l != 3 : print '\t'*l + "None"
    print ""
                
            
                
   
    
    
    
class Camera:
    zoom_step = 0.2
    z_level = 0
    zoom_limit = [0,3]
    view_box = [[0,0], [0,0]]
    orig_size = [0, 0]
    orig_box = [[0,0], [0,0]]
    move_step = 10.0 # how much we should move in proportion to view_box's size (currently 1/10 th)
    def __init__(self, tree):
        self.view_box = tree.bbox
        self.orig_box = tree.bbox
        self.orig_size = [tree.bbox[1][0] - tree.bbox[0][0], tree.bbox[1][1] - tree.bbox[0][1]]
        self.z_level = 0
        self.zoom_limit = [0,3]
        self.move_step = 10.0
    
    def __adjust(self):
        #trim it to original BBox
        if self.view_box[0][0] > self.orig_box[1][0]:
            self.view_box[0][0] -= self.orig_size[0]
            self.view_box[1][0] -= self.orig_size[0]
            
        if self.view_box[0][1] > self.orig_box[1][1]:
            self.view_box[0][1] -= self.orig_size[1]
            self.view_box[1][1] -= self.orig_size[1]

        if self.view_box[1][0] < self.orig_box[0][0]:
            self.view_box[0][0] += self.orig_size[0]
            self.view_box[1][0] += self.orig_size[0]
        
        if self.view_box[1][1] < self.orig_box[0][1]:
            self.view_box[0][1] += self.orig_size[1]
            self.view_box[1][1] += self.orig_size[1]
          
    def move(self, x, y):
        self.__move( x * self.size()[0] / self.move_step, y * self.size()[1] / self.move_step)
        
    def __move(self, x, y):
        self.view_box[0] = [self.view_box[0][0] + x, self.view_box[0][1] + y] 
        self.view_box[1] = [self.view_box[1][0] + x, self.view_box[1][1] + y]
        self.__adjust()        
            
    def __scale2(self, x_y):
        return self.orig_size[x_y] / 2.0 ** self.z_level
    def size(self):
        return [self.__scale2(0), self.__scale2(1)]
        
    def zoom(self, zoom_level, center = None):
        LOG("zooming ")
        if zoom_level < self.zoom_limit[0] or zoom_level > self.zoom_limit[1]:
            raise ValueError("Can't Adjust To the requested Zoom Value : ", zoom_level)
        self.z_level = zoom_level
        
        #zooming to the center of current view
        if center is None:
            center = [(self.view_box[0][0] + self.view_box[1][0]) / 2.0, (self.view_box[0][1] + self.view_box[1][1]) / 2.0]
        
        # center - (dist/z)/2, center + (dist/z)/2    
        new_size = self.size()
        half_size = [new_size[0] / 2.0, new_size[1] / 2.0]
        self.view_box = [[center[0] - half_size[0], center[1] - half_size[1]], [center[0] + half_size[0], center[1] + half_size[1]]]
    
    def __trim_zoom(self, z):
        if z > self.zoom_limit[1]:
            return self.zoom_limit[1]
        elif z < self.zoom_limit[0]:
            return self.zoom_limit[0]
        return z
        
    def zoom_in(self):
        self.zoom(self.__trim_zoom(self.z_level + self.zoom_step))
    def zoom_out(self):
        self.zoom(self.__trim_zoom(self.z_level - self.zoom_step))
    
    def __adjust_reverse_modulo_effect(self, value, x_y):
        if value < self.orig_box[0][x_y]:
            return value + self.orig_size[x_y]
        elif value > self.orig_box[1][x_y]:
            return value - self.orig_size[x_y]
        return value
        
    def adjust_reverses(self, point):
        tmp_x = point[0] + self.view_box[0][0]
        tmp_y = point[1] + self.view_box[0][1]
        #the camera can be in the range of [org_pos -orig_size ,orig_end_pos +orig_size] 
        #thus we need to trim it
        #cam start:-20 width:50,
        #orig start:0 end:100,
        #point to reverse :10 --> should be 90 in the new coordinat system
        return [self.__adjust_reverse_modulo_effect(tmp_x, 0),self.__adjust_reverse_modulo_effect(tmp_y,1)]
        
    def __adjust_to_coord_sys(self, point):
        tmp_x = point[0] - self.view_box[0][0]
        tmp_y = point[1] - self.view_box[0][1]
        #the camera can be in the range of [org_pos -orig_size ,orig_end_pos +orig_size] 
        #thus we need to trim it
        #cam start:-20 width:50,
        #orig start:0 end:100,
        #point:90 --> should be 10 in the new coordinat system
        return [tmp_x % self.orig_size[0], tmp_y % self.orig_size[1]]
    
    def adjust_to_coord_sys(self, point_list):
        return map(self.__adjust_to_coord_sys, point_list)        


class Display:
    width = 1280
    height = 720
    screen_area = 3/4.0
    scale = [0,0]
    
    #draw features    
    window = None
    background_color = (128,128,128)
    point_color = (255,255,0)
    line_color = (128,0,128)
    line_size  = 3

    def __init__(self, tree):
        self.screen_area = 3/4.0
        bbox = tree.bbox
        
        d_info = pygame.display.Info()
        if d_info.current_h != -1:
            self.height = d_info.current_h
        self.set_optimum_res((bbox[1][0] - bbox[0][0])/ (bbox[1][1] - bbox[0][1]), self.height)
        
        self.window =  pygame.display.set_mode((self.width, self.height))
        self.clear_screen()
        
    def set_optimum_res(self, ratio, max_H):
        self.width = int(round(max_H * self.screen_area * ratio))
        self.height = int(round(max_H * self.screen_area))
#        return [int(round(max_H * self.screen_area * ratio)), int(round(max_H * self.screen_area))]
        
    def scale_reverse(self, point):
        return [point[0] *  self.scale[0] /self.width  , point[1] * self.scale[1] /self.height ]
        
    def __scale_cord(self, point):
        return [point[0] * self.width / self.scale[0] , point[1] * self.height / self.scale[1]]
    def scale_cord(self, point_list):
        return map(self.__scale_cord, point_list)
        
    def draw_lines(self, point_list, color=None):
        pygame.draw.lines(self.window, color if color else self.line_color, False, point_list, self.line_size)
    def draw_points(self, point_list):
        for p in point_list:
           pygame.draw.rect(self.window, self.point_color, pygame.Rect(p[0], p[1] ,2,2)) 
    def clear_screen(self):
         self.window.fill(self.background_color)
         
    def flip_screen(self):
       #draw it to the screen
       pygame.display.flip() 
             
class Map:
    display = None    
    cam = None
    tree = None
    def __init__(self):
        self.tree = QTree(0, get_path(0,0,0))
        generate_Tree(0,0,0,self.tree)
        #explore(root)
        #print root.bbox
        #explore(root)
        #print QTree.count
        self.cam = Camera(self.tree)
        self.display = Display(self.tree)
    def draw_route(self, point_list, color):
        point_list = self.cam.adjust_to_coord_sys(point_list)
        point_list = self.display.scale_cord(point_list)
        corrupted = False
        last = point_list[0]
        for i in point_list:
            if abs(i[0] -last[0]) > self.display.width -200:
                corrupted = True
                break
            if abs(i[1] - last[1] ) > self.display.height - 200:
                corrupted = True
                break
            last = i
        if not corrupted:
           self.display.draw_lines(point_list, color)
            
    def draw(self, geo_data):
        for feature in geo_data['features']:
            if feature['geometry']['type'] == "GeometryCollection":
                for LineString in feature['geometry']['geometries']:
                    point_list = LineString['coordinates']
#                    print "Coordinates : \n", point_list
                    #shift the coordinate system
                    point_list = self.cam.adjust_to_coord_sys(point_list)
#                    print "adjust : \n", point_list
                    #scale the point list
                    point_list = self.display.scale_cord(point_list)
#                    print "scale : \n", point_list
                    corrupted = False
                    last = point_list[0]
                    for i in point_list:
                        if abs(i[0] -last[0]) > self.display.width -200:
                            corrupted = True
                            break
                        if abs(i[1] - last[1] ) > self.display.height - 200:
                            corrupted = True
                            break
                        last = i
#                        sys.stdout.write(str(int(i[1])) + ", ")
#                    print ""
                    if not corrupted:
                        self.display.draw_lines(point_list)
            elif feature['geometry']['type'] == "MultiPoint":
                point_list = feature['geometry']['coordinates']
                point_list = self.cam.adjust_to_coord_sys(point_list)
                point_list = self.display.scale_cord(point_list)
                self.display.draw_points(point_list)
#        print "\n"+ "*" * 30 + "\n"
    def draw_file(self, file_name):
        with open(file_name) as f:
            geo_data = json.load(f)
            self.draw(geo_data)
    def explore_list(self, item):
        if type(item) == list:
            for i in item:
                self.explore_list(i)
        elif type(item) == str:
            self.draw_file(item)
            
    def update(self, r):
        print "update Called zoom ", self.cam.z_level
        self.display.clear_screen()
        #update display scale to match the current zoom level
        self.display.scale = self.cam.size()
        
        file_list = self.tree.find_area(self.cam.z_level, self.cam.view_box)
#        print "f list \n", file_list
#        print "view ", self.cam.view_box
        self.explore_list(file_list)
        self.draw_route(r, (0,230,0))
        self.display.flip_screen()
        
    def zoom_in(self):
        self.cam.zoom_in()
    def zoom_out(self):
        self.cam.zoom_out()
    def move_to(self, dir):
        if dir == 'up':
            self.cam.move(0,-1)
        elif dir == 'down':
            self.cam.move(0,1)
        elif dir == 'right':
            self.cam.move(1,0)
        elif dir == 'left':
            self.cam.move(-1,0)
    def translate_pos_back(self, point):
        return self.cam.adjust_reverses(self.display.scale_reverse(point))
        
                
def main():
    city_graph = graph.Graph("path/path.data")
    print "done loading graph"
    pathF = pathfinder.PathPlanner(city_graph)
    print len(city_graph.vertex)
    route_id = pathF.Astar(0,100)
    route = []    
    for i in route_id:
        route.append(city_graph.vertex[i][graph.POS])
    print len(route)
    pygame.init() 
    m = Map()
    print m.display.width, m.display.height
    q = False
    m.update(route)
    path_point_id = [0,0]
    path_turn = True
    while not q: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                q = True
            if event.type == pygame.MOUSEBUTTONUP:
                pos =  m.translate_pos_back(event.pos)
                closest_id = closestpoint.manhattan(city_graph.vertex ,pos, 50)
                print "found closest pair", closest_id
                
                if path_turn:
                    path_point_id[0] = closest_id
                else : path_point_id[1] = closest_id
                path_turn = not path_turn
                
#                if path_turn:#we have set two points time to begin the fun!
#                    print "path finder result"
#                    print pathF.Astar(path_point_id[0], path_point_id[1])
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    print "BYE!"
                    q = True
                elif event.key == pygame.K_z: #zoom in
                    m.zoom_in()
                elif event.key == pygame.K_x: #zoom out
                    m.zoom_out()
                elif event.key == pygame.K_UP: #move
                    m.move_to('up')
                elif event.key == pygame.K_DOWN:
                    m.move_to('down')
                elif event.key == pygame.K_RIGHT:
                    m.move_to('right')
                elif event.key == pygame.K_LEFT:
                    m.move_to('left') 
                m.update(route)

    pygame.quit()
    
#def main_dbg():
#pygame.init()
#co = [[514986.58, 3951559.52], [516888.93, 3950900.13], [520815.36, 3948990.38], [520817.37, 3948990.52]]
#m = Map()
#m.update()
    
#tree = QTree(0, get_path(0,0,0))
#generate_Tree(0,0,0,tree)
#
#c = Camera(tree)
#view = [[514791.9936158612, 3949756.867333741], [567735.8536158613, 3982344.6373337405]]
#print [[514791, 3949756], [567735, 3982344]]
#f = tree.find_area(2.1, view)
if __name__ ==  "__main__": main()