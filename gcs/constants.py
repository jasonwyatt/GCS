from math import radians

#earth's mean radius
RADIUS_EARTH_M = 6371200.0
RADIUS_EARTH_KM = 6371.2

ARC_DEGREE_LAT = radians(RADIUS_EARTH_M)      #distance between two latitude

KM_TO_MAX_LATLNG = 1 / ARC_DEGREE_LAT

#from http://en.wikipedia.org/wiki/Longitude
WGS84_EQUATORIAL_RADIUS = 6378137.0 #meters
WGS84_POLAR_RADIUS = 6356752.3142 #meters