import unittest

from shapely.geometry import Point, LineString
from gcs.encoders.google_polyline import decode_polyline
from gcs import polyline, Polyline, LatLng

WIDTH_OF_ROAD_KM =  (3.6576 / 1000) #12 feet radius



class PolylineTestCase(unittest.TestCase):
    
    def testConstructor(self):
        start = LatLng(35.786100, -78.662430)
        end = LatLng(35.788140, -78.669680)
        
        poly = Polyline([start, end])                
        self.assertEqual(poly.first, start)
        self.assertEqual(poly.last, end)
        
        poly = Polyline((start, end))
        self.assertEqual(poly.first, start)
        self.assertEqual(poly.last, end)
        
        poly = Polyline(start, end)
        self.assertEqual(poly.first, start)
        self.assertEqual(poly.last, end)
    
    def testListMethods(self):
        poly = Polyline([LatLng(35.786100, -78.662430), LatLng(35.788140, -78.669680)])
        
        self.assertEquals(len(poly), 2)
        
        self.assertEqual(poly[0], poly.first)
        self.assertEqual(poly[-1], poly.last)
        
        a = LatLng(0, 0)
        b = LatLng(2, 2)
        
        poly[0] = a
        poly.last = b
        self.assertEqual(poly.first, a)
        self.assertEqual(poly.last, b)
        
        poly.prepend(a)
        poly.append(b)
        
        self.assertEquals(len(poly), 4)
        
        poly.insert(2, LatLng(3, 3))
        
        self.assertEquals(len(poly), 5)
        
        self.assertAlmostEquals(poly.bounds.north, 3)
        self.assertAlmostEquals(poly.bounds.south, 0)
        self.assertAlmostEquals(poly.bounds.west, 0)
        self.assertAlmostEquals(poly.bounds.east, 3)

    def testGeos(self):
        a = Point(0, 1)
        b = Point(1, 0)
        c = LineString([a.coords[0], b.coords[0]])
        
        poly = polyline.from_linestring(c.coords)
        
        self.assertEqual(poly.first, LatLng(a.y, a.x))
        self.assertEqual(poly.last, LatLng(b.y, b.x))

    def testInverse(self):
        poly = Polyline([LatLng(35.786100, -78.662430), LatLng(35.788140, -78.669680)])        
        
        poly_i = poly.inverse
        
        self.assertEqual(poly.first, poly_i.last)
        self.assertEqual(poly.last, poly_i.first)
        
    def testBounds(self):
        poly = Polyline([LatLng(35.786100, -78.662430), LatLng(35.788140, -78.669680)])        
        
        self.assertAlmostEqual(poly.bounds.north, 35.788140)
        self.assertAlmostEqual(poly.bounds.south, 35.786100)
        
        self.assertAlmostEqual(poly.bounds.west, -78.669680)
        self.assertAlmostEqual(poly.bounds.east, -78.662430)
    
    def testDistance(self):
        point1 = LatLng(37.739323, -122.473586)
        point2 = LatLng(37.749832, -122.453332)
                
        distance1 = Polyline(point1, point2).distance        
        assert round(distance1) == 2130.0, "distance calculation off."
        
        distance2 = Polyline(point1, point2, point1).distance
        assert round(distance2) == 4260.0, "distance calculation off."
        
    def testInterpolate(self):
        point1 = LatLng(37.739323, -122.473586)
        point2 = LatLng(37.749832, -122.453332)
        
        line = Polyline([point1, point2])
        
        assert line.interpolate(0.0) == point1
        assert line.interpolate(1.0) == point2
        
        try:
            line.interpolate(-1.0)
            assert False, "Shouldn't accept values < 0"
        except ValueError:
            pass
        
        half = line.interpolate(0.5)
        
        self.assertAlmostEquals(half.distance_to(point1), line.distance / 2, 3)
        assert half == LatLng(37.7445779332, -122.4634597190)


    def testSplit(self):
        polyline_str = "izwbEhu_nN|Bp@X}AyHoB_JqCq@bCk@bCvAiGp@iET}AqD}@vCeRxAkCPoA|AuJvCt@_AzEgCq@KCxBaMnDbAzKvCoApH~Bj@f@yCb@uCvHvBmAjHnBh@LBnAiHxFzArBp@iDzReBi@mD_AALy@`E}GcB_JmCu@S]]RsAAcBEyCJ_Add@xL~Ab@RgAf@yCnBd@tA^z@_F|Ab@zJhCpK`DfJ`CrGtB`BPbIzBdPfEnN`EO~@e@fCpPjEnHpB|A}J~AZx@PpHnCva@jLd@NbGq]rPdEc@`CiA`HoL}CcCo@zH{d@~JdCdKrCn`@vJtJnCzEwXfIe_@rCyNz@wFx@YjDj@~DClEeA`C_AvDeCzQwPdFoDrGaD|J{DnBeA`CaBzJsIjDsB`GmBfDYhGD~E`AtExAhNhDxDpB~M~I|Bz@jDd@p@TpFp@|AZfD|@|Dz@ZkGDuGZu@f@YtE@n@FvF`BGXFYkGeBkIIy@l^H\_@j[KfBmCdNy@zEcBpMgDtRMLWlAkAlHHVm@~EoIji@mFv^{I|f@WhAYf@aBY_NqD}@W|@yF^??{AHs@x@uEJIwD}@UDO@MDOf@~EnAs@jE?zA_@?}@xFqLcDk@G`@jD`BrKdAfEkBbARj@UnA~@NnC|@hA|Ah@W|@bAlCjBtAt@hC|@|q@rP|`@dKrDt@fIvBfDt@zEnBdDhCpBjCdCxFdAdE\tCDdEYxGk@hCc@Pe@@mAOKHi@dDcAtFvAZPj@B|@gS~cAUdBQ~ELnD`@jDlG`\zClPf@nDPjBP|EKzCqUuFuA`JZLgCzQvDz@Bi@m@qA?a@@QkB[cC~O@|@Z|@x@j@vEjAT^vAXt@Bx@a@n@}Ad@s@VKn@n@BhAcEvXMvBiBnuAu@tRQpA]fAo@nAy@|@y@l@qA`@yCRia@QuI|@a[lE_BN_B@}DWwDaAkCqAaCoBgAaAsBoC_EeI{Zet@iSae@sNs]wCmEoBuB{D_DqFyCulBst@iWkKiD{ByBeC{A_C}BmHi@iDUeDBcF|B_k@j@sM?y@UwCy@oCkAgB_AaAiAu@aBk@uDWoG`AyBEs@QcEqAcViK_\oJchAkZmDyAe@o@w@eBiE}PY{ETqG|@iJnQyhARcD?{Es@oFaCoHsDwNGiA_A{CgDuFyCmFy@m@kAIiAJc@FWZkAc@kGmAuIiCY|A{Bq@"
        poly = decode_polyline(polyline_str)
        
        splits = poly.split_at_angle()
        
        splits_sum = sum(a.distance for a in splits)
        self.assertAlmostEqual(splits_sum, poly.distance)
        
        self.assertEqual(poly, Polyline.concat_multiple(splits))
                
        

if __name__ == '__main__':
    unittest.main()