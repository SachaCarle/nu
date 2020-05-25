from .body import Body
from .mind import Mind
from .entity_class import Entity
from entity_stdlib import scripts
def std(*args):
    return {
        k: scripts[k] for k in args
    }