from .entity_class import Entity
from .handler import Handler
from pathlib import Path
from common import choice
import os, web, traceback

def card_(tx, style=None): return f"""
<div class="card" {"" if style == None else
"style='" + ';'.join([k + ": " + v for k, v in style.items()]) + ";'"
}>
  <div class="card-body">
  {tx}
  </div>
</div>
"""


class Synaps(Entity):
    Handler = Handler
    def createHandler(self):
        class virtual_Handler(self.__class__.Handler):
            synaps = self
        self.handler = virtual_Handler
# ------------------------------------------------------------- HANDLER
    def __call__(self, entity_class, *args, **kwargs):
        if isinstance(entity_class, type) and issubclass(entity_class, Entity):
            ne = entity_class(self, *args, **kwargs)
            if not ne.__class__.__name__ in self.by_class_entities:
                self.by_class_entities[ne.__class__.__name__] = []
            self.by_class_entities[ne.__class__.__name__].append(ne)
            return ne
        else:
            return Entity.__call__(self, entity_class, *args, **kwargs)
# ------------------------------------------------------------- ENTITY CREATION

    def __init__(self, *a, **b):
        Entity.__init__(self, self, *a, **b)
        self.by_class_entities = {}
    def getEntityLocation(self, e):
        return Path(os.getcwd(), e.name), Path(os.getcwd(), e.name, '.entity')
    def start(self, *args, **kwargs):
        self.createHandler(*args, **kwargs)
        self.app = web.application((
            '/(.*)', 'self',
        ), {'self': self.handler})
        self.app.run()


    def html_urlbar(self, path):
        return card_(f"""<h1><a href='/'>HOME</a> / <a>{path}</a></h1>
""")

    def html(self, path, *a, body=None, **b):
        A = self['head', path, a]
        B = self['urlbar', path]
        if body != None:
            C = body
        else:
            C = self['body', path, a, b]
        return f"""<!DOCTYPE html>
<html>
{A}
<body>
<div class='container'>
{B}
{C}
</div>
</body>
</html>"""

    def html_head(self, path, args):
        return f"""
    <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <!-- Add this to <head> -->

    <!-- Load required Bootstrap and BootstrapVue CSS -->
    <link type="text/css" rel="stylesheet" href="//unpkg.com/bootstrap/dist/css/bootstrap.min.css" />
    <link type="text/css" rel="stylesheet" href="//unpkg.com/bootstrap-vue@latest/dist/bootstrap-vue.min.css" />

    <title>{path}</title>
</head>
"""
    def html_body(self, path, *a):
        return self['class_list']

    def html_class_list(self):
        return f"""
{"<br>".join(["<h4>" + K + "</h4><br>" + self['entity_list', L, K]
    for K,L in self.by_class_entities.items()]) }
"""

    def html_entity_list(self, ets, name):
        s = f"<div class='{name}'>"
        for e in ets:
            try:
                s += card_(e['short'], style={'margin': "2px"})
            except Exception as er:
                _s = f"<p>{e.name}Exception: {repr(er)}<p><br>" + name + "<br>" + traceback.format_exc().replace('\n', '<br>')
                s += card_(_s)
            s += "" # br
        s += "</div>"
        return s
