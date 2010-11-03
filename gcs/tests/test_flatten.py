import unittest
import random

from shapely.geometry import Point
from gcs.tools.flattener import InterpolatedFlattener
from math import fabs

from gcs import LatLng
from gcs.encoders import google_polyline


poly_str = 'szkyEbma_NTWVSVSVGNAVAv@LrEnAh@F\?PETI^SRSJOHQHUH_@Dm@Ds@BkCCqBGkFIoHDsHDkGPcJB}DZqSgIIKfIMdN?XHXJRNPj@h@XZNLPXB^AxAQrIg@bOK|@iCxHu@fCk@dAsC`F'
poly1 = google_polyline.decode_polyline(poly_str)

MAX_DIFFERENCE = 100.0

class FlattenTestCase(unittest.TestCase):
    
    def _test_points(self, a, b):        
        geo_d = a[0].distance_to(b[0])
        cart_d = a[1].distance(b[1])
        difference = ((geo_d - cart_d) * 100000)
        difference = round(difference, 4)
        
            
        
        if fabs(difference) > MAX_DIFFERENCE:
            print '%s -> %s' % (a[0], b[0])
            print 'Correct Distance: %fkm' % geo_d
            print 'Interpolated Distance: %fkm' % cart_d
            print 'Difference: %.4fcm' % difference
        
        self.assertTrue(fabs(difference) <= MAX_DIFFERENCE)
            
        return geo_d, cart_d, difference
    
    def _test_area(self, bounds):
        '''
        Takes an area and tests how well gis to cartesion interpolation works
        '''
        view = InterpolatedFlattener.from_latlngboudns(bounds)    
    
        print 'Testing %s' % bounds
        
        print 'Widths (Top, Bottom): %fkm %fkm' % (bounds.north_width, bounds.south_width)        
        difference = bounds.south_width - bounds.north_width
        average_width =  (bounds.north_width + bounds.south_width) / 2.0
        print 'Width Difference: %fcm, %f%%' % ((difference * 100000), 100.0 * (difference / average_width))
        print 'Height: %fkm' % bounds.height
    
        
        nw = bounds.north_west
        ne = bounds.north_east
        sw = bounds.south_west
        se = bounds.south_east 
        center = bounds.center   
        
        def create_cart(geo):
            return (geo, Point(view.gis_to_cart_point(Point(geo.x, geo.y))))
        
        NW = create_cart(nw)
        NE = create_cart(ne)
        SW = create_cart(sw)
        SE = create_cart(se)
        CENTER = create_cart(center)
        
        self._test_points(NW, SW)    
        self._test_points(NW, NE)
        self._test_points(SW, SE)
        self._test_points(NW, SE)
        self._test_points(SW, NE)
        self._test_points(CENTER, SE)
    
        #test random points
        
        ds = []
        
        for _ in range(0, 1000):
            point1 = LatLng(random.uniform(bounds.north, bounds.south), random.uniform(bounds.east, bounds.west))
            point2 = LatLng(random.uniform(bounds.north, bounds.south), random.uniform(bounds.east, bounds.west))            
            _, _, d = self._test_points(create_cart(point1), create_cart(point2))
            ds.append(abs(d))
            
        print '%fcm, %fcm' % (max(ds), min(ds))


    def testArea1(self):
        bounds = poly1.bounds
        self._test_area(bounds)
        
        #test random points inside a bigger
        new_bounds = bounds.buffer(1.0)
        self._test_area(new_bounds)
