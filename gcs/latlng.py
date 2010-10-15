from math import sin, cos, sqrt, asin, atan2, radians, degrees, pi

from constants import ARC_DEGREE_LAT, RADIUS_EARTH_M
from gcs.utils import arcdegree_at_latitude_lng

from shapely.geometry import Point

SIGNIFICANT_DIGITS = 10

#the minimum difference between two latlngs for them to still be "equal" 
LAT_LNG_PRECISION = 10**-(SIGNIFICANT_DIGITS +1)

CLEAN_INT_TO_FLOAT = 10**-SIGNIFICANT_DIGITS

def clean_float(f):
    return int(round(f * 10**SIGNIFICANT_DIGITS))

class LatLng(object):
    '''
    A latitude longitude (y, x)
    
    Create a LatLng three different ways
    >>> point1 = LatLng(35, -78)    
    >>> point2 = LatLng((35, -78))
        
    Test that they are the same
    >>> point1 == point2
    True
    '''
    
    def __init__(self, arg0, arg1=None):
        if arg1 is None:
            try:
                #unpack arg0
                arg0, arg1 = arg0            
            except:
                raise TypeError('Invalid parameters given for LatLng initialization.')
        
        try:
            #clean the numbers to ensure that insignificant digits do not cause problems later on
            self._lat_clean = clean_float(arg0)            
            self._lng_clean = clean_float(arg1)
        except:
            raise TypeError('Invalid parameters given for LatLng initialization.')
        
        self._lat = self._lat_clean * CLEAN_INT_TO_FLOAT
        self._lng = self._lng_clean * CLEAN_INT_TO_FLOAT
            
    def __repr__(self):
        return 'LatLng(%f, %f)' % (self.lat, self.lng)
    
    def __unicode__(self):
        return '%f, %f' % (self.lat, self.lng)
    
    def __eq__(self, other):
        if other is None:
            return False
        
        if self is other:
            return True
        
        #if we know that the other object is a LatLng we can compare the clean values
        if other.__class__ is LatLng:
            return self._lat_clean == other._lat_clean and self._lng_clean == other._lng_clean
        
        return self._lat_clean == clean_float(other.lat) and self._lng_clean == clean_float(other.lat)

    def __ne__(self, other):        
        return not self.__eq__(other)
    
    def __hash__(self):
        return (self._lat_clean, self._lng_clean).__hash__() 
    
    def __iter__(self):
        yield self._lat
        yield self._lng
    
    @property
    def __geo_interface__(self):
        '''
        Provides a GeoJSON like interface
        '''
        return {'type': 'Point', 'coordinates': (self._lng, self._lat)}
    
    @property
    def point(self):        
        return Point(self._lng, self._lat)
    
    @property
    def lat(self):
        return self._lat
    
    @property
    def lng(self):
        return self._lng
    
    @property
    def lat_rad(self):
        return radians(self._lat)
        
    @property
    def lng_rad(self):
        return radians(self._lng)
    
    @property
    def tuple(self):
        return (self._lat, self._lng)
    
    @property
    def x(self):
        return self._lng
    
    @property
    def y(self):
        return self._lat
    
    @property
    def coords(self):
        '''
        Returns a tuple with cartesian coordinates (x,y)
        '''
        return (self._lng, self._lat)
    
    def buffer(self, d_km):        
          
        '''
        Returns a "square" centered at the current point that is at least 2 d_km X 2 d_km
        '''
        
        from latlngbounds import LatLngBounds        
        
        d_lat = d_km / ARC_DEGREE_LAT
        max_lat = self._lat + d_lat
        min_lat = self._lat - d_lat        
        
        theta = max_lat        
        if self.lat < 0.0:        #if below the equator cos(min_lat) is > than cos(max_lat)
            theta = min_lat
        
        d_lng = d_km / arcdegree_at_latitude_lng(theta)
        
        max_lng = self._lng + d_lng
        min_lng = self._lng - d_lng        
        
        return LatLngBounds(LatLng(min_lat, min_lng), LatLng(max_lat, max_lng))
        
    def angle_to(self, other, default=0.0):
        '''
        Calculates the angle from this point to another point
        '''
        
        if self == other:
            return default
        
        lat1 = self.lat_rad        
        lat2 = other.lat_rad
        dlng = other.lng_rad - self.lng_rad
        
        y = sin(dlng) * cos (lat2)
        x = (cos(lat1) * sin(lat2)) - (sin(lat1) * cos (lat2) * cos(dlng))            
        return atan2(y, x) % (2 * pi)

    def distance_to(self, other):
        '''
        Calculates the distance from this point to another point in meters using the haversine formula
        '''
                
        if self == other:
            return 0.0
                            
        lat1 = self.lat_rad
        lat2 = other.lat_rad        
        
        sin_dlat_over_2 = sin((lat2 - lat1) / 2.0)      
        sin_dlng_over_2 = sin((other.lng_rad - self.lng_rad) / 2.0)
        
        a = sin_dlat_over_2 * sin_dlat_over_2 + cos(lat1) * cos(lat2) * sin_dlng_over_2 * sin_dlng_over_2        
        return RADIUS_EARTH_M * 2.0 * asin(sqrt(a))

    
    def apply_bearing_and_distance(self, bearing, distance):
        '''
        Adds a bearing and a distance following the great circle art to the current point
        '''
        
        distance /= RADIUS_EARTH_M
        lat1 = self.lat_rad
        
        cos_d_r = cos(distance)
        sin_lat1 = sin(lat1)
        a = sin(distance) * cos (lat1)
        
        lat2 = asin(sin_lat1 * cos_d_r  +  a * cos(bearing))
        lng2 = self.lng_rad + atan2(sin(bearing) * a, cos_d_r - sin_lat1 * sin(lat2))
        return LatLng(degrees(lat2), degrees(lng2))    

if __name__ == "__main__":
    import doctest
    doctest.testmod()        