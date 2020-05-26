from .body import Body
from .body_scan import fs_scan
from .mind import Mind
from .entity_class import Entity

from entity_stdlib import scripts
def std(*args):
    return {
        k: scripts[k] for k in args
    }

from .entity_controller import Controller
from entity_stdlib.entities import *