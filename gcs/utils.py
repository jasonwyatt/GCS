from math import cos, radians, asin, sqrt, sin

from gcs.constants import RADIUS_EARTH_M, ARC_DEGREE_LAT


def arcdegree_at_latitude_lat(lat):
    '''
    Returns the arc distance between a degree of longitude at a given latitude
    '''  
    return cos(radians(i)) * ARC_DEGREE_LAT

def arcdegree_at_latitude_lng(lat):
    '''
    Dummy method so that the precise and simple functions can be swapped
    '''  
    return ARC_DEGREE_LAT


def arcdegree_at_latitude(lat):
    return (arcdegree_at_latitude_lat(lat), ARC_DEGREE_LAT)


from gcs.constants import WGS84_EQUATORIAL_RADIUS as E
from gcs.constants import WGS84_POLAR_RADIUS as P

PI_180 = radians(1.0)

def arcdegree_at_latitude_wgs84_lat(lat):
    '''
    Returns the arc distance between a degree of latitude at a given latitude
    '''
    
    lat = radians(lat)
    cos_lat = cos(lat)
    sin_lat = sin(lat)
    
    M = (P*E)**2 / ((E*cos_lat)**2 + (P*sin_lat)**2)**1.5
    return PI_180 * M
    
def arcdegree_at_latitude_wgs84_lng(lat):
    '''
    Returns the arc distance between a degree of longitude at a given latitude
    From http://en.wikipedia.org/wiki/Longitude
    '''
    lat = radians(lat)
    cos_lat = cos(lat)
    sin_lat = sin(lat)
    
    N = E**2 / (((E*cos_lat)**2 + (P*sin_lat)**2)**0.5)
    return PI_180 * cos_lat * N

def arcdegree_at_latitude_wgs84(lat):
    lat = radians(lat)
    cos_lat = cos(lat)
    sin_lat = sin(lat)
    
    J = (E*cos_lat)**2 + (P*sin_lat)**2    
    N = E**2 / J**0.5
    M = N * P**2 / J    
    
    return (PI_180 * M, PI_180 * cos_lat * N)
