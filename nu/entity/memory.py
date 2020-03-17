import sys, os, json
from flask import send_file
from pathlib import Path

def jsonoperate(loc):
    loc = Path(loc).resolve()
    def _jsonoperate(fun):
        d = {}
        if loc.exists():
            d = json.loads(loc.read_text())
            assert d, "empty data ?" + str(d)
        d = fun(d)
        os.remove(loc)
        with loc.open('w') as fd:
            json.dump(d, fd)
        print ('GOT', loc.read_text())
    return _jsonoperate

def alter(e):
    return jsonoperate(os.path.join(e.home, 'entity.json'))

def remember(e):
    def _remember(app):
        e.think ('I remember now... ' + str(e.components.data))
        for c in e.components.data:
            @e.head.define('/components/<path:p>')
            def __component_handler__(p):
                e.think('Requested component: ' + p + '\n\treturning file ' + str(Path(os.path.join(e.location, p)).resolve()) )
                return send_file(str(os.path.join(e.location, p)), mimetype='application')
        return e
    return _remember
