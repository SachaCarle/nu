from . import _, cmds, meta, entity
from pathlib import Path
import os.path

object = meta.obj
nupath = os.path.split(__file__)[0]
abpath = os.path.join(nupath, 'abstract')

def abstract(name):
    return Path(os.path.join(abpath, name)).read_text()

all = [
    "entity",
    "object",
    "abtract",
    "cmds",
    "nupath",
    '_'
]