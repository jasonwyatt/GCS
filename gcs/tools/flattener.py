from shapely.geometry import Point

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
    def from_tuple(cls, bounds):
        '''Convert from a shapely bounds (min_x, min_y, max_x, max_y)'''
        
        return cls(bounds[1], bounds[0], bounds[3], bounds[2])
    
    @classmethod
    def from_latlngbounds(cls, bounds):
        
        return cls(bounds.south, bounds.west, bounds.north, bounds.east)

    def initialize(self):
        pass
    
    def gis_to_cart_coord(self, coords):
        raise Exception("Not Implemented")
    
    def cart_to_gis_coord(self, coords):
        raise Exception("Not Implemented")
    
    def gis_to_cart_coords(self, coords):
        '''Converts latlng coords to cartesian coords'''
        
        return (self.gis_to_cart_coord(c) for c in coords)
            
    def cart_to_gis_coords(self, coords):
        '''Converts cartesian coords to a latlng'''
        
        return (self.cart_to_gis_coord(c) for c in coords)      
    
    def gis_to_cart_shape(self, shape):
        '''Converts a GIS shape to a cartesian shape'''
        
        try:
            coords = shape.coords
        except:
            coords = shape.__geo_interface__['coordinates']
     
        return shape.__class__(tuple(self.gis_to_cart_coords(coords)))
        
    def cart_to_gis_shape(self, shape):
        '''Converts a cartesian shape to a GIS one'''
        
        try:
            coords = shape.coords
        except:
            coords = shape.__geo_interface__['coordinates']
        
        return shape.__class__(tuple(self.cart_to_gis_coords(coords)))
    
    def gis_to_cart_point(self, point):
        '''Converts a lat,lng to a cartesian point'''
                
        try:
            coord = point.coords[0]
        except:
            coord = (point.__geo_interface__['coordinates'], )

        return Point(self.gis_to_cart_coord(coord))
    
    def cart_to_gis_point(self, point):
        '''Converts a cartesian point to a latlng'''    
        
        try:
            coord = point.coords[0]
        except:
            coord = (point.__geo_interface__['coordinates'], )           
        
        return Point(self.cart_to_gis_coord(coord))
    
class InterpolatedFlattener(GeoWindow):
    
    def initialize(self):        
        
        #find the middle latitude
        self.mid_lat = (self.max_lat + self.min_lat) / 2.0
        
        self.scale_y,  self.scale_x = wgs84.length_at(self.mid_lat)
        
        #keeps numbers small, not really needed
        self.translate_y = -self.min_lat 
        self.translate_x = -self.min_lng
    
    
    def gis_to_cart_coord(self, coord):
        '''Converts a latlng coord to cartesian coord'''
        
        x, y = coord
        x = (x + self.translate_x) * self.scale_x
        y = (y + self.translate_y) * self.scale_y
        return (x, y)
    
    def cart_to_gis_coord(self, coord):
        '''Converts a cartesian coords to a latlng'''
        
        x, y = coord
        x = (x / self.scale_x) - self.translate_x
        y = (y / self.scale_y) - self.translate_y
        return (x, y)
        
        
            
    