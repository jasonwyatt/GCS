from simplejson import encoder 

from . import LatLng, Polyline


class RoundedFloat(float):    
    def __repr__(self):
        return str(round(self, 6))    

class GcsJSONEncoder(encoder.JSONEncoder):
    '''
    A JSON Encoder that can encode geometry objects (LatLng, Polyline)
    '''
    
    callmap = {
            LatLng: 'encode_latlng',
            Polyline: 'encode_polyline'
            }
    
    def encode_latlng(self, object):
        return [RoundedFloat(n) for n in object.tuple]
    
    def encode_polyline(self, object):
        return [self.default(n) for n in object]
    
    def default(self, object):
        if object.__class__ not in self.callmap:
            return super(GcsJSONEncoder, self).default(object)
                
        method = getattr(self, self.callmap[object.__class__])
        return method(object)
        