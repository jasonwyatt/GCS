
from gcs import Polyline, LatLng

try:
    from shapely.geometry import LineString
except:
    pass

def encode_coords(coords):
    '''
    Encodes a polyline using Google's polyline algorithm
    http://code.google.com/apis/maps/documentation/polylinealgorithm.html
    '''
    
    result = []
    
    prev_lat = 0
    prev_lng = 0
    
    for coord in coords:
        d_lat, prev_lat = _encode_value(coord[1], prev_lat)
        d_lng, prev_lng = _encode_value(coord[0], prev_lng)        
        
        result.append(d_lat)
        result.append(d_lng)
    
    return ''.join(result)
    

def encode_polyline(polyline):
    return encode_coords([ll.coords for ll in polyline])
    
def encode_linestring(linestring):
    return encode_coords(linestring.coords)

def _encode_value(value, prev):
    #Step 2
    value = int(value * 1e5)
    value, prev = value - prev, value
    
    negative = (value < 0)
    
    #Step 4
    value <<= 1
    
    #Step - invert the encoding if negative
    if negative:
        value = ~value #
        
    #Step 6-7 - split into 5 bit chunks and reverse the order of the chunks
    chunks = []
    while value >= 32: #2^5, while there are at least 5 bits
        chunks.append(value & 31) # 2^5-1, zeros out all the bits other than the first five
        value >>= 5
    
    #Step 8 - OR each value with 0x20 if another bit chunk follows
    chunks = [chunk | 0x20 for chunk in chunks]
    
    #Complete step 6
    chunks.append(value) #append the last 5 bits
    
    #Step 9-10
    chunks = [chr(chunk + 63) for chunk in chunks]    
    
    return ''.join(chunks), prev

def decode(point_str):
    '''
    Decodes a polyline that has been encoded using Google's algorithm
    http://code.google.com/apis/maps/documentation/polylinealgorithm.html
    
    This is a generic method that returns a list of (x, y) tuples
    ''' or None
            
    #one coordinate offset is represented by 4 to 5 binary chunks
    coord_chunks = [[]]
    for char in point_str:
        
        #convert each character to decimal from ascii
        value = ord(char) - 63
        
        #values that have a chunk following have an extra 1 on the left
        split_after = not (value & 0x20)         
        value &= 0x1F
        
        coord_chunks[-1].append(value)
        
        if split_after:
                coord_chunks.append([])
        
    del coord_chunks[-1]
    
    coords = []
    
    for coord_chunk in coord_chunks:
        coord = 0
        
        for i, chunk in enumerate(coord_chunk):                    
            coord |= chunk << (i * 5) 
        
        #there is a 1 on the right if the coord is negative
        if coord & 0x1:
            coord = ~coord #invert
        coord >>= 1
        coord /= 100000.0
                    
        coords.append(coord)
    
    #convert the 1 dimensional list to a 2 dimensional list and offsets to actual values
    points = []
    prev_x = 0
    prev_y = 0
    for i in xrange(0, len(coords) - 1, 2):
        if coords[i] == 0 and coords[i + 1] == 0:
            continue
        
        prev_x += coords[i + 1]
        prev_y += coords[i]
        #a round to 6 digits ensures that the floats are the same as when they were encoded
        points.append((round(prev_x, 6), round(prev_y, 6)))
    
    return points    

def decode_polyline(point_str):
    '''Decodes a polyline that has been encoded using Google's algorithm
    Returns a Polyline object
    '''    
    latlngs = [LatLng(l[1], l[0]) for l in decode(point_str)]
    return None if len(latlngs) < 2 else Polyline(latlngs)

def decode_linestring(point_str):
    '''Decodes a polyline that has been encoded using Google's algorithm
    Returns a LineString object
    '''  
    points = decode(point_str)
    return None if len(points) < 2 else LineString(points)
    