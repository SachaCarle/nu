from . import _, cmds, meta, entity, components
from .moved import moved, duplicate
from .faith import workship
from pathlib import Path
import os.path

import string
drives=None
if "windows":
    from ctypes import windll

    def get_drives():
        drives = []
        bitmask = windll.kernel32.GetLogicalDrives()
        for letter in string.ascii_uppercase:
            if bitmask & 1:
                drives.append(letter)
            bitmask >>= 1
        return drives
    drives = get_drives()


object = meta.obj
#print ("HELLO WORLD", os.path.split(__file__))
nupath = os.path.split(__file__)[0]
abpath = os.path.join(nupath, 'abstract')

def abstract(name):
    return Path(os.path.join(abpath, name)).read_text()

all = [
    "entity",
    "meta", "object",
    "abtract",
    "components",
    "cmds",
    "nupath",
    '_',
    "drives",
    "moved",
    "workship",
]