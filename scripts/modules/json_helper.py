import json
import numpy 

class JsonHelper(json.JSONEncoder):
    def encode(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(JsonHelper, self).encode(obj)
