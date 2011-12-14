'''constants

Useful constants for GCS calculations.
'''

from math import radians as _radians

RADIUS_EARTH_M = 6371200.0
'''The Earth's mean radius in meters'''

RADIUS_EARTH_KM = 6371.2
'''The Earth's mean radius in kilometers'''

ARCDEGREE_LAT_LENGTH = _radians(RADIUS_EARTH_M)
'''Distance between two latitude values'''

KM_TO_MAX_LATLNG = 1 / ARCDEGREE_LAT_LENGTH
'''Maximum kilometers between two latitude values'''

WGS84_EQUATORIAL_RADIUS = 6378137.0 #meters
'''WGS84 equatorial radius of the earth in meters. from http://en.wikipedia.org/wiki/Longitude'''

WGS84_POLAR_RADIUS = 6356752.3142 #meters
'''WGS84 polar radius of the earth in meters. from http://en.wikipedia.org/wiki/Longitude'''
