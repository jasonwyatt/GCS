'''latlngbounds

Provides the LatLngBounds class.'''

from latlng import LatLng
from shapely.geometry import Polygon

class LatLngBounds(object):
    '''An isosceles trapezoid.
    '''
    
    def __init__(self, sw, ne=None): 
        self.south = sw.lat
        self.west = sw.lng
        
        if ne is None:
            self.north = sw.lat
            self.east = sw.lng
            
        else:
            self.north = ne.lat
            self.east = ne.lng
    
    def __eq__(self, other):
        if self is other:
            return True
        elif type(self) is not type(other):
            return False
        else:
            return (self.north_east == other.north_east and 
                    self.south_west == other.south_west)
    
    def __ne__(self, other):
        return not (other == self)
    
    def __str__(self):
        return '(south=%f, west=%f, north=%f, east=%f)' % (self.south, self.west, self.north, self.east)
    
    @property
    def north_east(self):
        return LatLng(self.north, self.east)
    
    @property
    def south_west(self):
        return LatLng(self.south, self.west)
    
    @property
    def north_west(self):
        return LatLng(self.north, self.west)
    
    @property
    def south_east(self):
        return LatLng(self.south, self.east)
    
    @property
    def height(self):
        return self.south_west.distance_to(self.north_west)
    
    @property
    def north_width(self):
        return self.north_west.distance_to(self.north_east)
                
    @property
    def south_width(self):
        return self.south_west.distance_to(self.south_east)
    
    @property
    def center(self):
        lat = self.south + (self.north - self.south) / 2
        lng = self.east + (self.west - self.east) / 2
        return LatLng(lat, lng)
    
    def buffer(self, value):
        sw = LatLng(self.south, self.west).buffer(value)
        ne = LatLng(self.north, self.east).buffer(value)        
        sw.north = ne.north
        sw.east = ne.east        
        return sw
    
    def expand(self, latlng):
        if self.north < latlng.lat:
            self.north = latlng.lat
        elif self.south > latlng.lat:
            self.south = latlng.lat
            
        if self.east < latlng.lng:
            self.east = latlng.lng
        elif self.west > latlng.lng:
            self.west = latlng.lng
    
    def union(self, other):
        north = max(self.north, other.north)
        east = max(self.east, other.east)
        south = min(self.south, other.south)
        west = min(self.west, other.west)
        
        return LatLngBounds(LatLng(south, west), LatLng(north, east))
    
    
    def contains(self, latlng):
        y = latlng.lat
        x = latlng.lng            
        return self.north >= y >= self.south and self.east >= x >= self.west     
    
    def to_polygon(self):
        origin = (self.west, self.south)
        return Polygon((
                        origin, 
                        (self.west, self.north), 
                        (self.east, self.north), 
                        (self.east, self.south),
                        origin
                        ))

__all__ = ['LatLngBounds']
