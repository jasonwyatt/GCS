'''spherical

Provides utility functions for calculating dimensions on a spherical coordinate 
system.
'''

from math import cos, radians

from gcs.constants import ARCDEGREE_LAT_LENGTH

def lng_length_at(lat):
    '''Returns the arc distance between a degree of longitude at a given 
    latitude.
    
    :param lat: Latitude
    :type lat: number
    :returns: Arc distance between a degree of latitude at a given latitude.
    :rtype: number
    
    '''  
    return cos(radians(lat)) * ARCDEGREE_LAT_LENGTH

def lat_length_at(lat):
    '''Dummy method so that the precise and simple functions can be swapped.  
    Returns the arc distance between a degree of latitude at a particular 
    latitude.
    
    :param lat: Latitude
    :type lat: number
    :returns: Arc distance between a degree of latitude at a given latitude.
    :rtype: number
    
    '''  
    return ARCDEGREE_LAT_LENGTH


def distance_at(lat):
    '''TODO: comment this.
    
    :param lat: Latitude
    :type lat: number
    :returns: TODO
    :rtype: tuple
    
    '''
    
    return (lng_length_at(lat), ARCDEGREE_LAT_LENGTH)
    
__all__ = ['lng_length_at', 'lat_length_at', 'distance_at']