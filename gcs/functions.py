from math import radians, sin, cos, asin, sqrt
from gcs.constants import RADIUS_EARTH_M

def distance(a, b):
    '''Calculates the distance between two points in meters using the haversine formula'''
            
    if a == b:
        return 0.0
                        
    lat1 = radians(a.y)
    lat2 = radians(b.y)
    
    sin_dlat_over_2 = sin((lat2 - lat1) / 2.0)      
    sin_dlng_over_2 = sin((radians(b.x - a.x)) / 2.0)
    
    a = sin_dlat_over_2 * sin_dlat_over_2 + cos(lat1) * cos(lat2) * sin_dlng_over_2 * sin_dlng_over_2        
    return RADIUS_EARTH_M * 2.0 * asin(sqrt(a))