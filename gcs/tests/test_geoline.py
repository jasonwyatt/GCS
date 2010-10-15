import unittest

from gcs import LatLng, GeoLine

class GelLineTestCase(unittest.TestCase):
    
    def testAngleTo(self):  
        a = LatLng(32.07605,-81.10437)
        b = LatLng(32.07542,-81.104620)
        c = LatLng(32.07529,-81.10415) 
        
        ab = GeoLine(a, b)
        bc = GeoLine(b, c)
        
        self.assertEqual(ab.angle_to(bc), bc.angle_to(ab))            

if __name__ == '__main__':
    unittest.main()