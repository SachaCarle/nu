from pathlib import Path
from common import choice
import os, web

from .root_entity import create_root_entity

class Synaps: # Entity ? Entity Interface ?
    create_root_entity = create_root_entity
    class Handler:
        def GET(self, *args, **kwargs):
            entity = self.root
            return entity('html', *args, **kwargs)
    def createHandler(self):
        class virtual_Handler(self.__class__.Handler):
            synaps = self
            root = self.re
        self.handler = virtual_Handler
# ------------------------------------------------------------- HANDLER
    def __call__(self, entity_class, *args, **kwargs):
        ne = entity_class(self, *args, **kwargs)
        if not ne.__class__.__name__ in self.by_name_entities:
            self.by_name_entities[ne.__class__.__name__] = []
        self.by_name_entities[ne.__class__.__name__].append(ne)
        return ne
# ------------------------------------------------------------- ENTITY CREATION

    def __init__(self):
        self.by_name_entities = {}
        self.re = self.create_root_entity()
    def getEntityLocation(self, e):
        return Path(os.getcwd(), e.name), Path(os.getcwd(), e.name, '.entity')
    def start(self, *args, **kwargs):
        self.createHandler(*args, **kwargs)
        self.re.start(*args, **kwargs)
        self.app = web.application((
            '/(.*)', 'self',
        ), {'self': self.handler})
        self.app.run()
    def head(self, path, *args, **kwargs):
        title = path if not 'title' in kwargs else kwargs['title']
        return f"""
    <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <!-- Add this to <head> -->

    <!-- Load required Bootstrap and BootstrapVue CSS -->
    <link type="text/css" rel="stylesheet" href="//unpkg.com/bootstrap/dist/css/bootstrap.min.css" />
    <link type="text/css" rel="stylesheet" href="//unpkg.com/bootstrap-vue@latest/dist/bootstrap-vue.min.css" />

    <title>{title}</title>
</head>
"""
