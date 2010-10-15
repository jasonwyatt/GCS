from gcs import Polyline

import operator

class GraphEdge():
    def __init__(self, polyline, from_node=None, to_node=None):
        self.polyline = polyline
        self.from_node = from_node
        self.to_node = to_node
        
    def split_by_nodes(self, nodes_inside, distance):
        if len(nodes_inside) == 0:
            return [self]
                                    
        new_points = []
        new_edges = []
        
        cur_node_i = 0                     
        prev_node = self.from_node        
        for i, point in enumerate(self.polyline):
            new_points.append(point)
                        
            while cur_node_i < len(nodes_inside):
                j = nodes_inside[cur_node_i][1][0]
                if i == j:
                    node, (_, _, exact) = nodes_inside[cur_node_i]
                    cur_node_i += 1
                   
                    if exact is True:
                        new_points[-1] = node.position                     
                    else:
                        new_points.append(node.position)
                    
                    new_edges.append(GraphEdge(Polyline(new_points), prev_node, node))
                    new_points = [node.position]                    
                    
                    prev_node = node
                else:
                    break
        
        if len(new_points) > 1:
            new_edges.append(GraphEdge(Polyline(new_points), prev_node, self.to_node))
        #otherwise there are two nodes at the same point
                     
        return new_edges
                    
class PolylineGraph(object):
    
    
    def __init__(self, segments, bounds):
        self.nodes = {}     #dict of nodes
        self.segments = {}  #dict of segments        
        self.links_from_nodes = {} #dict of sets, directional node -> segment -> other_node
        self.links_to_nodes = {} #dict of sets, directional other node -> segment -> node
        
        self.bounds = bounds
                       
        #Takes a number of segments and adds the segment to the nodes so that one can easily 
        #discover all the segments associated with a particular node                    
        map(self.add_segment, segments)
    
    def add_segment(self, segment):
        self.add_node(segment.from_node)
        self.add_node(segment.to_node)                
        
        self.segments[segment.id] = segment
        
        self.add_link_from_node(segment.from_node, segment)
        self.add_link_to_node(segment.to_node, segment)
                
    
    def add_link_from_node(self, node, segment):
        if not self.links_from_nodes.has_key(node.id):
            self.links_from_nodes[node.id] = set()
        
        self.links_from_nodes[node.id].add(segment.id)
        
    def add_link_to_node(self, node, segment):
        if not self.links_to_nodes.has_key(node.id):
            self.links_to_nodes[node.id] = set()
        
        self.links_to_nodes[node.id].add(segment.id)            
    
    def add_node(self, node, check=False):
        self.nodes[node.id] = node
        
        if check:        
            for new_link in node.links_from.all():
                self.add_segment(new_link)
            
            for new_link in node.links_to.all():
                self.add_segment(new_link)               
    
    def get_link_between(self, from_node, to_node):
        for link in self.get_links_from(from_node):
            if link.to_node == to_node:
                return link

    def get_links_from(self, from_node):
        if self.links_from_nodes.has_key(from_node.id):
            return [self.segments[id] for id in self.links_from_nodes[from_node.id]]
        return []
    
    def get_links_to_or_from(self, node):
        return self.get_links_from(node) + self.get_links_to(node)
    
    def get_links_to(self, to_node):
        if self.links_to_nodes.has_key(to_node.id):
            return [self.segments[id] for id in self.links_to_nodes[to_node.id]]
        return []
    
    def find_polyline_nodes(self, polyline, distance):
        '''
        Searches through a polyline and locates nodes that should divide it
        '''
        
        first = None
        last = None 
        inside = []
        
        #we may be able to match the first node and then walk down the tree
        #of current nodes, for now just brute force it
        for node in self.nodes.itervalues():
            if first == None and polyline.first.distance_to(node.position) <= distance:
                first = node
                continue
            elif last == None and polyline.last.distance_to(node.position) <= distance: 
                last = node
                continue
            
            snap = polyline.snap_point(node.position, distance)
            
            if snap is None:
                continue
            
            _, snap = snap
            
            inside.append((node, snap))
        
        #sort the nodes by where they occur in the segment
        inside = sorted(inside, key=operator.itemgetter(1))
                
        return first, last, inside 
        
            
    def split_polylines_at_nodes(self, polylines, distance):
        '''
        Split polylines that have a node between the first and last point
        '''
        #if we match the last node of a polyline then it can be used for the next segment,
        #try this later, if we assume that this is a path then this will always be true
        
        result = []
        
        for polyline in polylines:
            first, last, inside = self.find_polyline_nodes(polyline, distance)
            
            #append the polyline to the result, if it needs to be split then 
            #further polylines will be appended
            
            if first is not None and first.position != polyline.first:
                polyline.first = first.position
                
            if last is not None and last.position != polyline.last:
                polyline.last = last.position
            
            edge = GraphEdge(polyline, first, last)
            result += edge.split_by_nodes(inside, distance)
                    
        return result
    
    def get_partial_polyline_from(self, node, polyline, distance):
        for link in self.get_links_from(node):
            if link.shape.polyline.contains(polyline, distance):
                return link
        
    def get_partial_polyline_to(self, node, polyline, distance):
        for link in self.get_links_to(node):
            if link.shape.polyline.contains(polyline, distance):
                return link
        
