
from gcs import LatLng, Polyline

def encode_polyline(polyline):
    '''
    Encodes a polyline that has been encoded using Google's algorithm
    http://code.google.com/apis/maps/documentation/polylinealgorithm.html
    '''
    
    result = []
    
    prev_lat = 0
    prev_lng = 0
    
    for latlng in polyline:
        d_lat, prev_lat = _encode_value(latlng.lat, prev_lat)
        d_lng, prev_lng = _encode_value(latlng.lng, prev_lng)        
        
        result.append(d_lat)
        result.append(d_lng)
    
    return ''.join(result)

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
    
def decode_polyline(point_str):
    '''
    Decodes a polyline that has been encoded using Google's algorithm
    http://code.google.com/apis/maps/documentation/polylinealgorithm.html
    '''
            
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
    latlngs = []
    prev = LatLng(0, 0)
    for i in xrange(0, len(coords) - 1, 2):
        if coords[i] == 0 and coords[i + 1] == 0:
            continue
        
        prev = LatLng(prev.lat + coords[i], prev.lng + coords[i + 1])        
        latlngs.append(prev)
    
    return latlngs and Polyline(latlngs) or None
