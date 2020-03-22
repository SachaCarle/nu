import os
from pathlib import Path
from ..meta import obj
from .body import bodyset, show, move, duplicate
from .head import serve, awake, define
from .components import add
from .memory import alter, remember, load
from .father import pray

def think(e):
    def _think(*args, **kwargs):
        print(e.name + ':', *args, **kwargs)
    return _think

def infuse(entity):
    e = obj(entity)
    e.http = 'http://localhost:5000/'
    e.location = Path(os.getcwd(), '.entity').resolve()
    e.think = think(e)
    e.pray = pray(e)
    e.move = move(e)
    e.body = obj({
        'file': Path(e.location, 'body.html'),
        'set': bodyset(e),
        'show': show(e),
        'duplicate': duplicate(e),
    })
    e.memory = obj({
        'alter': alter(e),
        'remember': remember(e),
        'load': load(e),
    })
    e.components = obj({
        'add': add(e),
        **e.components
    })
    e.head = obj({
        'define': define(e),
        'routes': {},
    })
    e.serve = serve(e)
    e.awake = awake(e)
    try:
        return e.memory.remember(e)
    except Exception as er:
        print('Crashed...', entity)
        raise er