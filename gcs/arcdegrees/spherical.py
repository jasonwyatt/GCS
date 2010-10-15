from math import cos, radians

from gcs.constants import ARCDEGREE_LAT_LENGTH

def lng_length_at(lat):
    '''
    Returns the arc distance between a degree of longitude at a given latitude
    '''  
    return cos(radians(lat)) * ARCDEGREE_LAT_LENGTH

def lat_length_at(lat):
    '''
    Dummy method so that the precise and simple functions can be swapped
    '''  
    return ARCDEGREE_LAT_LENGTH


def distance_at(lat):
    return (lng_length_at(lat), ARCDEGREE_LAT_LENGTH)