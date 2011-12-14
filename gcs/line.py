'''line

Provides the GeoLine and GeoLineSnap classes
'''

from math import sin, cos, pi

class GeoLineSnap():
    def __init__(self, point, distance_from_initial, distance_from_start, snapped_after_end):
        self.point = point
        self.distance_from_initial = distance_from_initial #distance from the initial point
        self.distance_from_start = distance_from_start #distance from the start
        self.snapped_after_end = snapped_after_end #a snap that is under the threshold beyond the end is allowed to snap

class GeoLine(object):
    
    def __init__(self, start, end):
        self._start = start
        self._end = end        
        self._distance = None
        self._angle = None        
    
    def __eq__(self, other):
        return self.start == other.start and self.end == other.end
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __repr__(self):            
        return 'GeoLine(%s,%s)' % (repr(self.start), repr(self.end))
    
    @property
    def start(self):
        return self._start
    
    @property
    def end(self):
        return self._end
    
    @property
    def distance(self):
        if self._distance is None:
            self._distance = self.start.distance_to(self._end)
        return self._distance
    
    @property
    def angle(self):
        if self._angle is None:
            self._angle = self.start.angle_to(self._end)
        return self._angle
    
    @property
    def inverse(self):
        result = GeoLine(self._end, self._start)
        
        if self._distance is not None:
            result._distance = self._distance
            
        return result
    
    @property
    def polyline(self):
        '''Converts the GeoLine into a Polyline
        '''
        from . import Polyline
        return Polyline([self.start, self.end])
    
    @property
    def points(self):
        return (self._start, self._end)
    
    def _clean_angle(self, angle):
        '''Ensures that an angle is always between 0 and pi
        
        '''        
        angle = abs(angle) % (2 * pi)
        
        if angle > pi:
            return (2 * pi) - angle        
        return angle

    
    def snap_point(self, point, max_distance, snap_beyond=True):
        '''Finds the closest point on line, the distance to that point from the 
        previous point and how far
        (snap latlng, distance from line, distance from start 
        If snap_beyond is true then points that are beyond the last points will be snapped
        '''
        
        hypotenuse = GeoLine(self._start, point)
        theta = self.angle_to(hypotenuse)        
                
        if theta > (pi / 2): 
            return None
                
        adjacent_length = cos(theta) * hypotenuse.distance        
        result_point = self.point_at_distance(adjacent_length)        
        snap_length = sin(theta) * hypotenuse.distance
        
        if snap_length < max_distance:
            if adjacent_length <= self.distance and adjacent_length >= 0.0:
                return GeoLineSnap(result_point, snap_length, adjacent_length, False)
            
            #if we did snap beyond the line, make sure the snap distance was less than the max_distance 
            if snap_beyond and adjacent_length > self.distance and adjacent_length - self.distance < max_distance:
                snap_length = point.distance_to(self.end)
                if snap_length < max_distance:                
                    return GeoLineSnap(self.end, snap_length, self.distance, True)            
            
        return None
    
    def closest_point(self, target):
        '''Returns the point on the line closest to target.
        
        '''
        from constants import RADIUS_EARTH_KM
        linesnap = self.snap_point(target, RADIUS_EARTH_KM)
        if linesnap is None or target.distance_to(self.start) < linesnap.distance_from_initial:
            return self.start
        else:
            return linesnap.point
    
    def angle_to(self, other):
        '''Calculates the smallest angle between two lines which have to points 
        in common
        
        '''
        
        if not self.is_connected_with(other):
            raise ValueError("Two points must be the same to calculate angle.")
        
        return self._clean_angle(self.angle - other.angle)                 
    
    def is_connected_with(self, other):
        '''Tests whether two GeoLines share an endpoint
        
        '''
        if self.start == other.start or self.end == other.end:
            return True
        elif self.end == other.start or self.start == other.end:
            return True
        return False
    
    def delta_angle(self, other):
        '''Finds the change in direction in radians between the lines.
        
        More or less 180 - angle_to(), but not quite. Very useful for finding 
        abrupt changes in direction.
        
        '''
        assert self.end == other.start, "Lines must be connected to measure angle delta."
        
        translated = GeoLine(self.end, self.point_at_distance(2 * self.distance))
        angle = translated.angle_to(other)
        return angle
    
    def point_at_distance(self, new_length):
        '''Returns the point at a given distance from the start
        
        '''
        return self._start.apply_bearing_and_distance(self.angle, new_length)
        
__all__ = ['GeoLineSnap', 'GeoLine']
    