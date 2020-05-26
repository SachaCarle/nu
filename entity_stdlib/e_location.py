from entity import Entity, body_scan, std
from pathlib import Path
from os import getcwd


class Location(Entity):
    LOCATION_PATH_KEY = 'location_path'
    def __init__(self, path, **defs_body_data):
        if isinstance(path, str):
            self.name = path
            path = Path(getcwd(), path).resolve()
        else:
            self.name = '<anonyme>'
            path = Path(getcwd(), path).resolve()
        assert isinstance(path, Path), 'Invalid path: ' + repr(path)
        assert not self.LOCATION_PATH_KEY in defs_body_data, self.LOCATION_PATH_KEY + ' key is used by Location(Entity)'
        defs_body_data[self.LOCATION_PATH_KEY] = str(path)
        path.mkdir(parents=True, exist_ok=True)
        assert path.is_dir(), repr(path) + 'is not a valid folder.'
        final_body_data = {**std('watchdog', 'create_location'), **body_scan.fs_scan(path), **defs_body_data}
        Entity.__init__(self, **final_body_data)
    def __str__(self):
        return f"<Location: {self.name}>"





#!