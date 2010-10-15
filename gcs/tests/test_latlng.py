import unittest

from math import pi
from gcs import LatLng, GeoLine

WIDTH_OF_ROAD_KM =  (3.6576 / 1000) #12 feet radius

SIGNIFICANT_PLACES = 3 #milimeter precision

class LatLngTestCase(unittest.TestCase):
    
    def testBuffer(self):  
        distance_m = 5000.0
              
        point = LatLng(35.0, 78.0)                
        bounds = point.buffer(distance_m)
        
        self.assertAlmostEqual(bounds.height, distance_m * 2, SIGNIFICANT_PLACES)
        
        min_width = min(bounds.north_width, bounds.south_width)
        max_width = min(bounds.north_width, bounds.south_width)
        
        self.assertAlmostEqual(max_width, distance_m * 2, SIGNIFICANT_PLACES)    
    
    def testApplyAngleAndBearing(self):
        start = LatLng(35.786100, -78.662430)
        end = LatLng(35.788140, -78.669680)
        
        bearing = start.angle_to(end)
        distance = start.distance_to(end)
                
        test_end = start.apply_bearing_and_distance(bearing, distance)
        
        self.assertEqual(test_end, end)
    

class LineTestCase(unittest.TestCase):

    def testIsBetween(self):
        not_between = LatLng(35.786960, -78.666960)
        
        start = LatLng(35.786100, -78.662430)
        end = LatLng(35.788140, -78.669680)
        
        line = GeoLine(start, end)
        
        self.assertEquals(line.snap_point(not_between, WIDTH_OF_ROAD_KM), None)  
        
    def __testSnap(self, start, mid, end):
        line = GeoLine(start, end)
        
        snap = line.snap_point(mid, WIDTH_OF_ROAD_KM)
        self.assertNotEqual(snap, None)
        
        actual_distance = mid.distance_to(snap.point)
        
        self.assertAlmostEqual(snap.distance_from_initial, actual_distance)
        
        self.assertAlmostEqual(snap.distance_from_start, start.distance_to(snap.point))
    
    def __testSnapBad(self, start, mid, end):
        line = GeoLine(start, end)
        
        snap = line.snap_point(mid, WIDTH_OF_ROAD_KM)
        self.assertEqual(snap, None)

    
    def testSnapBad(self):
        mid = LatLng(35.786960, -78.666960)
        
        start = LatLng(35.786100, -78.662430)
        end = LatLng(35.788140, -78.669680)
                
        self.__testSnapBad(end, mid, start)
        self.__testSnapBad(start, mid, end)
    
    def testSnapGood(self):
        mid = LatLng(35.787350, -78.666755)
        
        start = LatLng(35.786100, -78.662430)
        end = LatLng(35.788140, -78.669680)
                
        self.__testSnap(end, mid, start)
        self.__testSnap(start, mid, end)
        
    def testInverse(self):
        start = LatLng(35.786100, -78.662430)
        end = LatLng(35.788140, -78.669680)
        
        line = GeoLine(start, end)        
        inverse = line.inverse
        
        self.assertEqual(line.start, inverse.end)
        self.assertEqual(line.end, inverse.start)
        
        #test when line.angle and line.distance are not cached        
        self.assertEqual(line.distance, inverse.distance)     
        uncached_line_angle = line.angle
        uncached_inverse_angle = (inverse.angle + pi) % (2 * pi)
        self.assertAlmostEqual(uncached_inverse_angle, uncached_line_angle, 3)
        
        #test using cached line and angle
        inverse = line.inverse
        self.assertEqual(line.distance, inverse.distance)

if __name__ == '__main__':
    unittest.main()