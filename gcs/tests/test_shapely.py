from shapely.geometry import asShape

import unittest

from gcs import Polyline, LatLng

class PolylineTestCase(unittest.TestCase):
    
    def testLatLng(self):
        shp = asShape(LatLng(35, -78))        
        self.assertEqual(shp.type, 'Point')
        self.assertEqual(shp.coords[0], (-78.0, 35.0))
            
    def testPolyline(self):
        shp = asShape(Polyline(LatLng(33, 40), LatLng(34, 41)))
        self.assertEqual(shp.type, 'LineString')
    