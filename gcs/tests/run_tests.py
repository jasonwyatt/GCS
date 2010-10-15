#!/usr/bin/python

import unittest
from test_latlng import LatLngTestCase
from test_polyline import PolylineTestCase
from test_polyline_snap import PolylineSnapTestCase

def all_tests():
    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(LatLngTestCase),
        unittest.TestLoader().loadTestsFromTestCase(PolylineTestCase),
        unittest.TestLoader().loadTestsFromTestCase(PolylineSnapTestCase),         
    ])

if __name__ == '__main__':
    tests = all_tests()
    failures = unittest.TextTestRunner(verbosity=2).run(tests)