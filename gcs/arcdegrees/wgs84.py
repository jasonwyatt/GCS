'''wgs84

Provides utility functions for calculating dimensions on a wgs84 coordinate 
system.
'''

from math import cos, radians, sin

from gcs.constants import WGS84_EQUATORIAL_RADIUS as E
from gcs.constants import WGS84_POLAR_RADIUS as P

PI_180 = radians(1.0)

def lng_length_at(lat):
    '''Returns the length of an arcdegree of longitude at a given latitude.
    From http://en.wikipedia.org/wiki/Longitude
    
    :param lat: Latitude
    :type lat: number
    :returns: Length of an arcdegree of longitude.
    :rtype: number
    
    '''
    lat = radians(lat)
    cos_lat = cos(lat)
    sin_lat = sin(lat)
    
    N = E**2 / (((E*cos_lat)**2 + (P*sin_lat)**2)**0.5)
    return PI_180 * cos_lat * N

def lat_length_at(lat):
    '''Returns the length of an arcdegree of latitude at a given latitude.
    
    :param lat: Latitude
    :type lat: number
    :returns: Length of an arcdegree of latitude.
    :rtype: number
    
    '''
    
    lat = radians(lat)
    cos_lat = cos(lat)
    sin_lat = sin(lat)
    
    M = (P*E)**2 / ((E*cos_lat)**2 + (P*sin_lat)**2)**1.5
    return PI_180 * M
    
def length_at(lat):
    '''Returns (length of an arcdegree of latitude, length of an arcdegree of 
    longitude) at a given latitude.
    
    TODO: maybe re-name this to distance_at?
    
    :param lat: Latitude
    :type lat: number
    :returns: 2-tuple containing (length of an arcdegree of latitude, length of 
    an arcdegree of longitude)
    :rtype: tuple
    
    '''
    
    lat = radians(lat)
    cos_lat = cos(lat)
    sin_lat = sin(lat)
    
    J = (E*cos_lat)**2 + (P*sin_lat)**2    
    N = E**2 / J**0.5
    M = N * P**2 / J    
    
    return (PI_180 * M, PI_180 * cos_lat * N)
    
__all__ = ['length_at', 'lat_length_at', 'lng_length_at']
