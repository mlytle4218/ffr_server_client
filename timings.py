import json

class Timings:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        
    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)