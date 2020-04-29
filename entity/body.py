from pathlib import Path

class Body(dict):
    def __getitem__(self, key):
        v = dict.__getitem__(self, key)
        if isinstance (v, Path):
            return v.resolve().read_text()
        return v
    def __setitem__(self, key, value):
        pass # NOT SET ?
    def __init__(self, entity, body_data):
        dict.__init__(self, body_data)
