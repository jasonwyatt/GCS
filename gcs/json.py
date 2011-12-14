'''json

Provides a JSON Encoder for LatLng and Polyline objects.

'''
try:
    from json import encoder
except ImportError:
    from simplejson import encoder 

from . import LatLng, Polyline


class RoundedFloat(float):    
    def __repr__(self):
        return str(round(self, 6))    

class GcsJSONEncoder(encoder.JSONEncoder):
    '''A JSON Encoder that can encode geometry objects (LatLng, Polyline)
    
    Public functions:
    encode_latlng -- Encodes a LatLng object into a JSON-ready list.
    
    encode_polyline -- Encodes a Polyline object into a JSON-ready list.
    
    '''
    
    callmap = {
            LatLng: 'encode_latlng',
            Polyline: 'encode_polyline'
            }
    
    def encode_latlng(self, object):
        '''Encode a LatLng object into a JSON-ready list.
        
        @type   object: LatLng
        @param  object: LatLng Object to Encode
        
        @rtype: list
        @returns: A List, containing the latitude and longitude of the 
        argument, rounded to 6 decimal places.
        
        '''
        return [RoundedFloat(n) for n in object.tuple]
    
    def encode_polyline(self, object):
        '''Encode a Polyline object into a JSON-ready list.
        
        @type   object: Polyline
        @param  object: Polyline Object to Encode
        
        @rtype: list
        @returns: A List, containing lists with the latitude and longitude of 
        the points along the polyline, rounded to 6 decimal places.
        
        '''
        return [self.default(n) for n in object]
    
    def default(self, object):
        '''Encodes an object to JSON'''
        
        if object.__class__ not in self.callmap:
            return super(GcsJSONEncoder, self).default(object)
                
        method = getattr(self, self.callmap[object.__class__])
        return method(object)
        
__all__ = ['GcsJSONEncoder']
