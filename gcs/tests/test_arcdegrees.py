import unittest
from gcs.arcdegrees import spherical, wgs84

#from http://en.wikipedia.org/wiki/Longitude
#Latitude
#N-S radius of curvature M
#Length of one degree latitude
#E-W radius of curvature N
#Length of one degree longitude
real_data = [
             [0,    6335.44,    110.574,    6378.14,    111.320],
             [15,   6339.70,    110.649,    6379.57,    107.551], 
             [30,   6351.38,    110.852,    6383.48,    96.486],
             [45,   6367.38,    111.132,    6388.84,    78.847],
             [60,   6383.45,    111.412,    6394.21,    55.800],
             [75,   6395.26,    111.618,    6398.15,    28.902], 
             [90,   6399.59,    111.694,    6399.59,    0.000]
] 

class ArcDegreeTestCase(unittest.TestCase):
    
    def testLatLng(self):
        for lat, _, lat_d, __, lng_d in real_data:
            lat_d *= 1000
            lng_d *= 1000            
            
            self.assertAlmostEquals(lat_d, spherical.lat_length_at(lat), places=-4)
            self.assertAlmostEquals(lat_d, wgs84.lat_length_at(lat), places=-1)
            
            self.assertAlmostEquals(lng_d, spherical.lng_length_at(lat), places=-4)
            self.assertAlmostEquals(lng_d, wgs84.lng_length_at(lat), places=-1)
            
            ad_lat, ad_lng = wgs84.length_at(lat)
            
            self.assertAlmostEquals(ad_lat, wgs84.lat_length_at(lat))
            self.assertAlmostEquals(ad_lng, wgs84.lng_length_at(lat))
            
            
            
    