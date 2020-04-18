from pathlib import Path
import os

class Synaps: # Entity ? Entity Interface ?
    def __call__(self, entity_class, *args, **kwargs):
        return entity_class(self)
    def getEntityLocation(self, e):
        return Path(os.getcwd(), e.name), Path(os.getcwd(), e.name, '.entity')