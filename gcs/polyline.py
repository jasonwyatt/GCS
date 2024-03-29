'''polyline

Provides the Polyline, PolylineSnap, and SnapOptions classes, as well as the 
from_linestring utility function.
'''

from itertools import izip

from math import radians

from line import GeoLine
from latlng import LatLng
from latlngbounds import LatLngBounds

def from_linestring(linestring):
    return Polyline([LatLng(p[1], p[0]) for p in linestring])

class PolylineSnap():
    def __init__(self, point, distance_from_initial, distance_from_index, index, exact_snap):
        self.point = point
        self.distance_from_initial = distance_from_initial
        self.distance_from_index = distance_from_index
        self.index = index
        self.exact_snap = exact_snap
        self.polyline_distance = None

class SnapOptions():
    def __init__(self, **kwargs):        
        self.max_distance = 0.015 #15 meters, the maximum distance from the polyline to snap        
        self.snap_beyond = True #whether to snap beyond the last endpoint of the polyline 
        
        for key in kwargs:
            try:
                setattr(self, key, kwargs[key])
            except AttributeError:
                pass
            

class Polyline(object):
    '''A ordered list of LatLngs that form a shape
    
    Create a Polyline two different ways
    >>> poly1 = Polyline(LatLng(35, -78), LatLng(36, -78))    
    >>> poly2 = Polyline([LatLng(35, -78), LatLng(36, -78)])
    >>> poly3 = Polyline([(35, -78), (36, -78)])
    
    '''
    
    def __init__(self, *args):  
        '''Creates a new instance of a Polyline
        
        :param args: varargs for the polyline. Each one shoud be either a 
        LatLng or a tuple containing (latitude, longitude)
        
        '''      
        if len(args) == 1:
            args = args[0]        
        
        #check that the input is iterable
        if not hasattr(args, '__iter__'):        
            raise TypeError('Invalid parameters given for Polyline initialization. %s' % type(args))
                
        self._points = list(Polyline.clean_points(args))
        
        if not len(self._points):
            raise TypeError('Polyline must be initialized with at least one point.')
                
        if len(self._points) == 1:
            #if only one point was added then add it twice
            self._points.append(self._points[0])        
        
        self.__on_shape_changed()
    
    def __iter__(self):
        '''Iterator that iterates over the points in the Polyline
        
        '''
        for latlng in self._points:
            yield latlng
    
    def __eq__(self, other):
        '''Determines whether or not this polyline is equal to the supplied 
        object.
        
        :param other: Other object
        :returns: Whether or not this Polyline is equal to the supplied object.
        :rtype: bool
        
        '''
        if not other:
            return False
        
        return len(other) == len(self) and all(p == s for p, s in izip(self, other))        
    
    def __ne__(self, other):
        '''Determines whether or not this Polyline is not-equal to the supplied 
        object.
        
        :param other: Other object
        :returns: Whether or not this Polyline is not-equal to the supplied 
        object.
        :rtype: bool
        
        '''
        return not self.__eq__(other)
    
    def __copy__(self):
        '''Creates a copy of the Polyline
        
        :returns: A copy of this Polyline.
        :rtype: Polyline
        
        '''
        return Polyline(self._points)
    
    def __len__(self):
        '''Gets the length of the Polyline (the number of points in the 
        Polyline)
        
        :returns: Number of points in the Polyline
        :rtype: number
        
        '''
        return len(self._points)
        
    def __getitem__(self, index):
        '''Gets a particular point at a supplied index along the Polyline
        
        :param index: Index of the point along the Polyline
        :type index: number
        :returns: Point along the Polyline at the specified index.
        :rtype: LatLng
        
        '''
        return self._points[index]

    def __setitem__(self, index, value):
        '''Sets the point at the specified index to the specified point 
        (LatLng).
        
        :param index: Index along the Polyline to change the point for.
        :type index: number
        :param value: New point for the specified index.
        :type value: LatLng
        
        '''
        if not value.__class__ is LatLng:
            raise Exception("Item must be a LatLng")
        
        self._points[index] = value
        self.__on_shape_changed()
    
    def __repr__(self):        
        '''Creates a human-readable string containing the information about the 
        Polyline.
        
        :returns: Human-readable representation of the Polyline
        :rtype: string
        
        '''
        
        return 'Polyline(%s)' % ','.join(repr(point) for point in self)
    
    @staticmethod
    def from_coords(coords):
        '''Creates a polyline from a list/tuple of cartesian coordinates.
        
        :param coords: List of coordinates, where each coordinate is a 
        tuple/list with x/y coordinates (longitude, latitude)
        :type coords: list
        :returns: Polyline constructed from supplied coordinates.
        :rtype: Polyline
        
        '''
        try:
            return Polyline(LatLng(p[1], p[0]) for p in coords)
        except:
            raise Exception("Unable to create a Polyline from given coordinates")
        
    @staticmethod
    def concat_multiple(polys):
        '''Concatenates multiple Polylines into a single Polyline
        
        :param polys: List of Polyline objects
        :type polys: list
        :returns: New Polyline that consists of all of the points in all of the 
        supplied Polylines concatenated together.
        :rtype: Polyline
        
        '''
        
        if not polys:
            return None
        
        return Polyline(point for poly in polys for point in poly)
    
    @staticmethod    
    def clean_points(points):
        '''Generator: turns a list of points into LatLng objects. The list can 
        contain either tuples/lists or LatLng objects.
        
        :param points: List of points
        :type points: list
        
        '''
        prev = None
        for point in points:
            if point == prev:
                continue
            
            yield point if point.__class__ == LatLng else LatLng(*point)
            
            prev = point            
    
    @property
    def __geo_interface__(self):
        '''Provides a GeoJSON like interface useful with Shapely.
        
        :returns: Dictionary containing the object type, and a list of 
        coordinates.
        :rtype: dict
        
        '''
        return {'type': 'LineString', 'coordinates': tuple(self.coords)}
    
    def get_first(self):
        '''Gets the first point in the Polyline
        
        :returns: First point in the Polyline
        :rtype: LatLng
        
        '''
        return self[0]
        
    def set_first(self, latlng):    
        '''Sets the first point in the Polyline to the supplied LatLng.
        
        :param latlng: New value for the first point.
        :type latlng: LatLng
        
        '''
        self[0] = latlng
    
    first = property(get_first, set_first)
    
    def get_last(self):
        '''Gets the last point in the Polyline
        
        :returns: Last point in the Polyline
        :rtype: LatLng
        
        '''
        return self[-1]
    
    def set_last(self, latlng):
        '''Sets the last point in the Polyline
        
        :param latlng: New value for the last point.
        :type latlng: LatLng
        
        '''
        
        self[-1] = latlng
    
    last = property(get_last, set_last)
    
    @property
    def bounds(self):
        '''Property to retrieve the bounding box of the Polyline
        
        :returns: Bounding box of the Polyline
        :rtype: LatLngBounds
        
        '''
        if not self._bounds:
            result = None
            for latlng in self:
                if not result:
                    result = LatLngBounds(latlng)
                else:
                    result.expand(latlng)
            
            self._bounds = result
        return self._bounds
    
    @property
    def lines(self):
        '''Returns a tuple containing all the pairs of points in the polyline.
        
        For a polyline with n points this should be n - 1
        If a polyline consists of points A, B, & C this would yield 
            [GeoLine(A, B), GeoLine(B, C), GeoLine(B, C)]
            
        :returns: Tuple containing all pairs of points in the polyline as 
        GeoLine objects.
        :rtype: tuple
        
        '''
        
        if not self._lines:
            self._lines = tuple(GeoLine(A, B) for (A, B) in zip(self._points[:-1], self._points[1:]))
        return self._lines
            
    @property
    def angles(self):
        '''Yields all of the angles that exist in the polyline as a list of tuples
        
        For a polyline with n points this should be n - 2
        If a polyline consists of points A, B, & C this would return (AB, BC)
        
        '''
        prev = None
        for cur in self.lines:
            if prev is not None:
                yield (prev, cur) 
            prev = cur
            
    @property
    def lines_reversed(self):
        '''Generator that yields the GeoLines that make up the Polyline's line 
        segments, in reverse order.
        
        '''
        i = len(self) - 1
        while i > 0:            
            yield GeoLine(self[i],  self[i-1])
            i -= 1
               
    @property
    def coords(self):
        '''Provides a cartesian set of coordinates for use with GEOS.
        
        :returns: Tuple containing the points along the Polyline.
        :rtype: tuple
        
        '''
        return (pt.coords for pt in self._points)
    
    @property
    def distance(self):
        '''Returns the total length of the Polyline in KM.
        
        :returns: Total length of the polyline, in Kilometers.
        :rtype: number
        
        '''
        if self._distance is None:
            self._distance = sum(line.distance for line in self.lines)
        
        return self._distance
    
    @property
    def inverse(self):
        '''Returns the polyline in reverse.
        
        :returns: Reversed polyline
        :rtype: Polyline
        
        '''
        return Polyline(reversed(self._points))
    
    @property
    def points(self):
        '''Returns a tuple containing all of the points in the Polyline
        
        :returns: Tuple containing each point in the Polyline
        :rtype: Polyline
        
        '''
        return tuple(pt for pt in self)
    
    def __on_shape_changed(self):
        '''Called when the shape of the polyline has been altered.
        
        Clears things that are cached.
        
        '''
        self._bounds = None
        self._distance = None
        self._lines = None
    
    def append(self, value):
        '''Adds a single point to the end of this polyline.
        
        >>> p = Polyline()
        >>> ll = LatLng(35, -80)
        >>> p.append(ll)
        
        :param value: New point to append to the Polyline.
        :type value: LatLng
        
        '''        
        self._points.append(value)
        self.__on_shape_changed()
        
    def prepend(self, value):
        '''Adds a single point to the beginning of this polyline.
        
        >>> p = Polyline(LatLng(34, -80), LatLng(34.5, -80))
        >>> ll = LatLng(35, -80)
        >>> p.prepend(ll)
        
        :param value: New point to prepend onto the Polyline.
        :type value: LatLng
        
        '''        
        self._points.insert(0, value)
        self.__on_shape_changed()        
    
    def insert(self, index, object): 
        '''Inserts a new point at the specified index of the Polyline.
        
        >>> p = Polyline(LatLng(34, -80), LatLng(35, -80))
        >>> ll = LatLng(34.5, -80)
        >>> p.insert(1, ll)
        
        :param index: Index where the new point should be inserted.
        :type index: number
        :param object: New point to insert.
        :type object: LatLng
        
        '''       
        self._points.insert(index, object)
        self.__on_shape_changed()    
    
    def add(self, other):
        '''Adds the points from this polyline with those from another to form a 
        new longer polyline.
        
        :param other: Other Polyline
        :type other: Polyline
        :returns: New polyline, consisting of this Polyline, plus the other 
        Polyline
        :rtype: Polyline
        
        '''  
        if self.last == other.first:
            #chop the first point off the other polyline so that we don't end up with duplicate points
            return Polyline(self._points + list(other)[1:])
        else:
            return Polyline(self._points + list(other))
    
    def interpolate(self, ratio):
        '''Returns the point at ratio distance into the polyline. 
        
        0.0 returns the first point, 1.0 returns the last point.
        
        :param ratio: Distance ratio along the length of the Polyline
        :type ratio: number
        :returns: Interpolated point along the Polyline at the specified 
        distance ratio.
        :rtype: LatLng
        
        '''
        if not (0.0 <= ratio <= 1.0):
            raise ValueError("Ratio must be between 0.0 and 1.0")
        
        interp_distance = self.distance * ratio
        for line in self.lines:
            if interp_distance <= line.distance:
                return line.point_at_distance(interp_distance)
            else:
                interp_distance -= line.distance
        
        # We got all the way to the end; we shouldn't have any slacking length
        assert round(interp_distance, 4) == 0.0, "interp_distance: %f != 0.0" % interp_distance
        return self.last
        
    
    def splice(self, other):
        '''Splices a polyline to the end or beginning of this one. Ensures that 
        the order of points for this polyline stays the same, the other 
        polyline will be reversed if necessary.
        
        One of the endpoints of the other Polyline must match one of the 
        endpoints of this Polyline.
        
        :param other: Other polyline to splice onto this polyline.
        :type other: Polyline
        :returns: New polyline, the result of this polyline spliced with the 
        other.
        :rtype: Polyline
        
        '''
        if self.first == other.last:
            return other.add(self)
        elif self.last == other.first:
            return self.add(other)
        elif self.first == other.first:
            return other.inverse.add(self)
        elif self.last == other.last:
            return self.add(other.inverse)
        
        raise Exception("Cannot splice polylines together, endpoints do not match")
    
    def splice_fuzzy(self, other):
        '''Like splice, but doesn't require endpoints match exactly.
        
        :param other: Other polyline to splice onto this polyline.
        :type other: Polyline
        :returns: New polyline, the result of this polyline spliced with the 
        other.
        :rtype: Polyline
        
        '''
        pairings = (
            (self.last, other.first, self.add(other)),
            (self.last, other.last, self.add(other.inverse)),
            (self.first, other.last, other.add(self)),
            (self.first, other.first, other.inverse.add(self)),
        )
        closest = 1e99
        best = None
        for left, right, result in pairings:
            dist = left.distance_to(right)
            if dist < closest:
                closest = dist
                best = result        

        return best
    
    def closest_vertex(self, point):
        '''Returns the closest vertex in the polyline to the given point.
        
        :param point: Point to find the closest vertex for.
        :type point: LatLng
        :returns: Closest vertex point to the supplied point.
        :rtype: LatLng
        
        '''
        return min(self, key=lambda x: point.distance_to(x))
    
    def closest_point(self, point):
        '''Returns the closest point on the polyline to the given point,
        regardless of distance.
        
        :param point: Point to find the clsest point along the polyline for.
        :type point: LatLng
        :returns: Closest point on the Polyline (not necessarily a vertex)
        :rtype: LatLng
        
        '''
        candidates = [L.closest_point(point) for L in self.lines]
        return min(candidates, key=lambda x: x.distance_to(point))
    
    def split_at_angle(self, threshold=radians(60)):
        '''Splits the polyline wherever the change in direction angle is 
        greater than the threshold. Returns a list of polylines.
        
        :param threshold: Threshold angle, in radians, where the polyline 
        should be split.
        :type threshold: number
        :returns: List of polylines that are the result of splitting.
        :rtype: list
        
        '''
        if len(self) <= 2:
            return [list(self)]

        # the first line starts us off
        result = [self[:2]]
        
        for A, B in self.angles:
            # make sure it's at least a meter b/c angles aren't sensible at that
            # size.
            if A.distance >= 0.001 and B.distance >= 0.001 and A.angle_to(B) > threshold:
                # we have a turn, break it up here
                result.append(list(B.points))
            else:
                # still on the same path. tack it onto the last
                result[-1].append(B.end)

        return [Polyline(points) for points in result]
    
    def split_at(self, index):
        '''Splits the polyline and returns the Polyline beyond the split point.
        
        :param index: Point index along the polyline where the split should 
        occur.
        :type index: number
        :returns: Tail of the Polyline that was split off.
        :rtype: Polyline
        
        '''
        old_points = self._points
        
        self._points = self._points[:index + 1]
        self.__on_shape_changed()
        
        return Polyline(old_points[index:])
                    
    def split_at_point(self, point, threshold):
        '''Splits the polyline and returns the Polyline beyond the split point.
        
        Unlike split_at(index), this will split at any point along the Polyline 
        instead of at an exact vertex index.
        
        :param point: Point to split at.
        :type point: LatLng
        :param threshold: TODO: comment this attribute
        :type threshold: number
        :returns: Tail of the Polyline that was split off.
        :rtype: Polyline
        
        '''
        cur_buffer = [self.first]
        new_buffer = []
        has_split = False
        
        for line in self.lines:
            if has_split:
                new_buffer.append(line.end)                
            elif point.is_between(line.start, line.end, threshold):
                has_split = True
                cur_buffer.append(point)
                new_buffer.append(point)
                new_buffer.append(line.end)
            else:
                cur_buffer.append(line.end)
        
        if len(new_buffer) > 1:             
            self._points = cur_buffer
            self.__on_shape_changed()
            return Polyline(new_buffer)
    
    def snap_point_all(self, latlng, options=None):
        ''''Finds the closets points on the polyline that is within the 
        max_distance of the given point.
        
        :param latlng: TODO: comment this attribute
        :type latlng: LatLng
        :param options: Options for snapping.
        :type options: SnapOptions
        :returns: TODO: comment the return value.
        :rtype: TODO: comment the return type.
        
        '''
        
        options = options if options else SnapOptions()
        max_distance = options.max_distance
        
        #simple check that it is within the bounds
        if not (self.bounds.contains(latlng) or self.bounds.buffer(max_distance).contains(latlng)):
            return []
                    
        lines = list(self.lines)        
        snaps = []
        
        #simple check that the other point is exactly one of the polyline points
        for i, point in enumerate(self):
            if latlng == point:
                snaps.append(PolylineSnap(point, 0.0, 0.0, i, True))
                
        if not len(snaps):                
            for i, line in enumerate(lines):
                snap_beyond = options.snap_beyond or (i < len(lines) - 1)                     
                snap = line.snap_point(latlng, max_distance, snap_beyond)
                            
                if snap is None:                
                    continue
                
                if snap.point == line.start:                
                    cur_snap = PolylineSnap(snap.point, snap.distance_from_initial, 0.0, i, True)
                elif snap.point == line.end:                
                    cur_snap = PolylineSnap(snap.point, snap.distance_from_initial, 0.0, i + 1, True)                
                else:                
                    cur_snap = PolylineSnap(snap.point, snap.distance_from_initial, snap.distance_from_start, i, False)
                
                snaps.append(cur_snap)
                
        for snap in snaps:            
            distance = snap.distance_from_index
            for i, line in enumerate(lines):
                if i >= snap.index:
                    break
                distance += line.distance
            snap.polyline_distance = distance
         
        return sorted(snaps, key=lambda snap: snap.distance_from_initial)
    
    def snap_point(self, latlng, options=None):
        """Snaps a point using snap_point_all into the polyline that the point 
        snapped.
        
        :param latlng: Point to snap onto the Polyline
        :type latlng: LatLng
        :param options: Options for snapping.
        :type options: SnapOptions
        :returns: Snapped point.
        :rtype: LatLng
        
        """
        snaps = self.snap_point_all(latlng, options)
        if not snaps:
            return None
        return snaps[0]
        
    def contains(self, other, max_distance):
        '''Determines if this segment contains another one.
        
        :param other: Other Polyline.
        :type other: Polyline
        :param max_distance: Maximum distance to allow for snapping.
        :type max_distance: number
        :returns: Whether or not the other polyline can snap onto this 
        Polyline.
        :rtype: bool
        
        '''
        
        for latlng in other:
            snap = self.snap_point(latlng, SnapOptions(max_distance=max_distance)) 
            if snap is None:
                return False
                
        return True
    
    def subtract_from(self, other, max_distance):
        '''Returns the points that are in the other polyline that are not part 
        of this one.
        
        :param other: Other Polyline.
        :type other: Polyline
        :param max_distance: Maximum distance to allow for snapping.
        :type max_distance: number
        :returns: List of Polylines for the points on the other Polyline that 
        couldn't be snapped (weren't "part" of this polyline)
        :rtype: list
        
        '''
        
        self_list = list(self)
        other_list = list(other)
        other_reversed = False
        
        if self.first == other.first:
            pass
        elif self.last == other.last:
            self_list.reverse()
            other_list.reverse()
            other_reversed = True
        elif self.first == other.last:            
            other_list.reverse()  
            other_reversed = True
        elif self.last == other.first:
            self_list.reverse()                                        
        else:
            return [other]
        
        
        cur = self_list[0]
        self_i = 1
        other_i = 1
        broken = False
        
        new_path = [cur]
        result = [new_path]
        
        #run until we have looked at all the points in the other polyline
        while other_i < len(other_list):
            #if we have run out of points in this polyline then add the remaining ones from other to the output
            if self_i >= len(self_list):
                new_path += other_list[other_i:]   
                break
            
            
            self_next = self_list[self_i]
            other_next = other_list[other_i]
            
            if broken is True:
                #after a break, check all the remaining points on self to find one that snaps to the other
                                
                #try to snap remaining points from this polyline on the other one
                snap = other.snap_point(self_next, max_distance) 
                if snap is not None:
                    _, (snap_pos, _, _) = snap
                    cur = self_next
                    
                    #check if the other polyine snaps first
                    while other_i <= snap_pos - 1:
                        other_prev = other_list[other_i]
                        other_cur = other_list[other_i + 1]
                        
                        if other_cur.is_between(other_prev, cur, max_distance):
                            cur =  other_cur
                            break
                        
                        new_path.append(other_cur)                        
                        other_i += 1
                    
                    new_path.append(cur)                        
                    broken = False
                else:    
                    self_i += 1
            
            else: #not broken
                if self_next == other_next:
                    cur = self_next
                    self_i += 1
                    other_i += 1
                    new_path.append(cur)
                    continue
                
                #given cur, a point we know is on both polylines, find which polyline has the
                #next closest point
                if cur.distance_to(other_next) < cur.distance_to(self_next):
                    closest = other_next
                    farthest = self_next
                else:
                    closest = self_next
                    farthest = other_next
                
                #check if the closest point lies between the current point and the farthest
                #if it does not then we have found a break
                if closest.is_between(cur, farthest, max_distance):
                    cur = closest
                    
                    if closest == other_next:                        
                        other_i += 1
                else: 
                    broken = True
                    
                    if new_path[-1] != cur:
                        new_path.append(cur)
                    new_path = [cur]
                    result.append(new_path)
                
                if closest == self_next:
                    self_i += 1
                
        if len(result[0]) == 1:
            return [other]
        
        if len(new_path) == 1:
            result.pop()
        
        if other_reversed is True:
            result.reverse()           
            [path.reverse() for path in result]
            
        return [Polyline(path) for path in result]


__all__ = ['from_linestring', 'Polyline', 'PolylineSnap', 'SnapOptions']
