import sys, os, json, nuthon
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
        assert isinstance(d, dict), "Please return data from @e.memory.alter !!!"
        assert not (d in [None, 'null', '{}', {}, False, True])
        os.remove(loc)
        with loc.open('w') as fd:
            json.dump(d, fd)
    return _jsonoperate

def alter(e):
    return jsonoperate(os.path.join(e.location, 'entity.json'))

def remember(e):
    def _remember(app):
        e.think('What am I ?', list(e.keys()))
        e.think ('Where I am ?..\t' + str(e.location))
        e.think ('I remember now... ' + str(e.components.data))
        for c in e.components.data:
            @e.head.define('/components/<path:p>')
            def __component_handler__(p):
                e.think('Maybe I should this routes only for ' + str(c))
                e.think('Requested component: ' + p + '\n\treturning file ' + str(Path(os.path.join(e.location, p)).resolve()))
                return send_file(str(os.path.join(e.location, p)), mimetype='application')
        return e
    return _remember

def load(e):
    def _load(path):
        p = Path(os.path.split(e.location)[0], path).resolve()
        res = nuthon.imp(path, e)
        return res
    return _load