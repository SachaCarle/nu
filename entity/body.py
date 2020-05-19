from pathlib import Path
from os import remove

class Body(dict):
    def __getitem__(self, key):
        v = dict.__getitem__(self, key)
        if isinstance (v, Path):
            return v.resolve().read_text()
        return v
    def __setitem__(self, key, value):
        if isinstance(value, Path):
            value = value.resolve().absolute()
        # No override ?!
        # / No override file
        if key in self:
            v = dict.__getitem__(self, key)
            if isinstance(v, Path):
                return v.write_text(value)
        assert not key in self, "Key already set: " + repr(key)
        dict.__setitem__(self, key, value)
    def __init__(self, entity, body_data):
        body_data = { k: v.resolve().absolute() if isinstance(v, Path) else v
            for k, v in body_data.items()}
        dict.__init__(self, body_data)
