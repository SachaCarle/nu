from . import _, cmds, meta, entity, components
from pathlib import Path
import os.path

object = meta.obj
#print ("HELLO WORLD", os.path.split(__file__))
nupath = os.path.split(__file__)[0]
abpath = os.path.join(nupath, 'abstract')

def abstract(name):
    return Path(os.path.join(abpath, name)).read_text()

all = [
    "entity",
    "object",
    "abtract",
    "components",
    "cmds",
    "nupath",
    '_'
]