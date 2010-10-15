from . import Polyline, LatLng

from shapely import wkb

class PolylineShapeFormat:    
    WKB=0
    WKT=1
    Polyline=2
    LineString=3

def parse_wkb_polyline(geom_wkb, format):
    geom_wkb = geom_wkb.decode('hex')
    
    if format == PolylineShapeFormat.WKB:
        return geom_wkb 
    
    geom_wkb = wkb.loads(geom_wkb)
    if format == PolylineShapeFormat.LineString:
        return geom_wkb
    elif format == PolylineShapeFormat.WKT:
        return geom_wkb.wkt
    
    return Polyline.from_coords(geom_wkb.coords)

class PointShapeFormat:    
    WKB=0
    WKT=1
    LatLng=2
    Point=3
