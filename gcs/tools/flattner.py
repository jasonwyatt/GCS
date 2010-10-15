from shapely.geometry import LineString, Point

from gcs.arcdegrees import wgs84
        
class GeoWindow():
    '''
    Flattens a GIS area so that points are in cartesian rather than in a square  
    '''
    
    def __init__(self, min_lat, min_lng, max_lat, max_lng):
        self.min_lat = min_lat
        self.min_lng = min_lng
        self.max_lat = max_lat
        self.max_lng = max_lng      
        
        self.initialize()
    
    @classmethod    
    def from_tuple(c, bounds):
        '''
        Convert from a shapely bounds (min_x, min_y, max_x, max_y)
        '''
        return c(bounds[1], bounds[0], bounds[3], bounds[2])
    
    @classmethod
    def from_latlngboudns(c, bounds):
        return c(bounds.south, bounds.west, bounds.north, bounds.east)

    def initialize(self):
        pass
    
    def gis_to_cart_shape(self, shape):
        '''
        Converts a GIS shape to a cartesian shape 
        '''
        
        points = shape.__geo_interface__['coordinates']
        return LineString(tuple(self.gis_to_cart_point(Point(p)).coords[0] for p in points))
        
    def cart_to_gis_shape(self, shape):
        '''
        Converts a cartesian shape to a GIS one
        '''
        points = shape.__geo_interface__['coordinates']
        return LineString(tuple(self.cart_to_gis_point(Point(p)).coords[0] for p in points))
    
    def gis_to_cart_point(self, point):
        '''
        Converts a lat,lng to a cartesian point
        '''        
        return point
    
    def cart_to_gis_point(self, point):
        '''
        Converts a cartesian point to a latlng
        '''    
        return point
    
class InterpolatedFlattner(GeoWindow):
    
    def initialize(self):        
        
        #find the middle latitude
        self.mid_lat = (self.max_lat + self.min_lat) / 2.0
        
        self.geo_ratio_y,  self.geo_ratio_x = wgs84.length_at(self.mid_lat)
        
        #keeps numbers small, not really needed
        self.geo_min_y = self.min_lat 
        self.geo_min_x = self.min_lng                
    
    def gis_to_cart_point(self, point):
        '''
        Converts a lat,lng to a cartesian point
        '''
        x = (point.x - self.geo_min_x) * self.geo_ratio_x
        y = (point.y - self.geo_min_y) * self.geo_ratio_y        
        
        return Point(x, y)
    
    def cart_to_gis_point(self, point):
        '''
        Converts a cartesian point to a latlng
        '''    
        
        x = (point.x / self.geo_ratio_x) + self.geo_min_x
        y = (point.y / self.geo_ratio_y) + self.geo_min_y
        
        return Point(x, y)
    