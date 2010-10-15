import unittest

from gcs import LatLng, SnapOptions
from gcs.encoders import google_polyline

class PolylineSnapTestCase(unittest.TestCase):
    
    def __snap(self, point, encoded_polyline, options, result):
        polyline = google_polyline.decode_polyline(encoded_polyline) 
        
        #self.assertFalse(polyline.bounds.contains(point))
        snap = polyline.snap_point(point, options)
        
        if result:        
            self.assertNotEqual(snap, None)            
        else:
            self.assertEqual(snap, None)
            
        return snap            
    
    def testGoodSnaps(self):
        options = SnapOptions(max_distance=15.0/1000)
                
        self.__snap(LatLng(30.435380, -91.168733), "{ivxDhmmkPeBVm@J[H_A^k@Xi@PW@W?k@I_@S{EmD_@Sm@Qk@CQA]Be@F{Bh@cAN", options, True)
        
        options.max_distance = 0.1
        
        self.__snap(LatLng(42.32541, -71.179567), "esiaG|qlqLeB]AjAFh@Ax@AtAGfAEvAIj@Gf@Kl@Sz@zCdC", options, True)
        
        #this point is just outside of the last point of the polyline
        self.__snap(LatLng(42.337333, -71.103065), "g_laG~h~pL}PoKa@g@", options, True)
        
        self.__snap(LatLng(42.35902, -71.093656), "usnaGrt{pLem@zU_CfAsCvBoBtCu`@zw@", options, True)
        
        self.__snap(LatLng(42.359099, -71.093506), "usnaGrt{pLem@zU_CfAsCvBoBtCu`@zw@", options, True)
        
        
    
    def testBadSnaps(self):
        options = SnapOptions(max_distance=15.0/1000)
        
        self.__snap(LatLng(30.5, -91.168733), "{ivxDhmmkPeBVm@J[H_A^k@Xi@PW@W?k@I_@S{EmD_@Sm@Qk@CQA]Be@F{Bh@cAN", options, False)        
    

if __name__ == '__main_2_':
    unittest.main()