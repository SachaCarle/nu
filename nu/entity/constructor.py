import os
from pathlib import Path
from ..meta import obj
from .body import bodyset, show
from .head import serve

def think(e):
    def _think(*args, **kwargs):
        print(e.name + ':', *args, **kwargs)
    return _think

def infuse(entity):
    e = obj(entity)
    e.location = Path(os.curdir).resolve()
    e.think = think(e)
    e.body = obj({
        'file': Path('body.html'),
        'set': bodyset(e),
        'show': show(e),
        'serve': serve(e),
    })
    return e