from pathlib import Path
from common import choice
import os, web

from .root_entity import create_root_entity

class Synaps: # Entity ? Entity Interface ?
    class Handler:
        def GET(self, *args, **kwargs):
            entity = self.root
            entity('think', args, kwargs)
            return entity('html', *args, **kwargs)
    def createHandler(self):
        class virtual_Handler(self.__class__.Handler):
            synaps = self
            root = self.re
        self.handler = virtual_Handler

    def __init__(self):
        self.by_name_entities = {}
        self.re = create_root_entity(self)
    def __call__(self, entity_class, *args, **kwargs):
        ne = entity_class(self)
        if not ne.name in self.by_name_entities:
            self.by_name_entities[ne.name] = []
        self.by_name_entities[ne.name].append(ne)
        return ne
    def getEntityLocation(self, e):
        return Path(os.getcwd(), e.name), Path(os.getcwd(), e.name, '.entity')
    def start(self, *args, **kwargs):
        self.createHandler(*args, **kwargs)
        self.re.start(*args, **kwargs)
        self.app = web.application((
            '/(.*)', 'self',
        ), {'self': self.handler})
        self.app.run()
