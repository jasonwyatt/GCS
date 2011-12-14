'''functions

Utility functions for GCS operations.
'''

from math import radians, sin, cos, asin, sqrt
from gcs.constants import RADIUS_EARTH_M

def distance(a, b):
    '''Calculates the distance between two coordinates in meters using the haversine formula
    
    Example:
    
    >>> from gcs.functions import distance
    >>> from gcs import LatLng
    >>> x = LatLng(35, -80)
    >>> y = LatLng(36, -80)
    >>> distance(x, y)
    111198.41730306287
    
    :param a: First coordinate.
    :type a: LatLng
    :param b: Second coordinate.
    :type b: LatLng
    :returns: A number, theistance between the two coordinates (in meters) via the Haversine Formula.
    :rtype: number
    '''
            
    if a == b:
        return 0.0
                        
    lat1 = radians(a.y)
    lat2 = radians(b.y)
    
    sin_dlat_over_2 = sin((lat2 - lat1) / 2.0)      
    sin_dlng_over_2 = sin((radians(b.x - a.x)) / 2.0)
    
    a = sin_dlat_over_2 * sin_dlat_over_2 + cos(lat1) * cos(lat2) * sin_dlng_over_2 * sin_dlng_over_2        
    return RADIUS_EARTH_M * 2.0 * asin(sqrt(a))

def _test():
    import doctest
    doctest.testmod()
    
if __name__ == '__main__':
    _test()
    
__all__ = ['distance']
