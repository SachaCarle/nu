import json
from pathlib import Path
# --
from . import constructor

def spirit(entityfile):
    jsontxt = Path(entityfile).read_text()
    entity = json.loads(jsontxt)
    return constructor.infuse(entity)

