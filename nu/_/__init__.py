from . import logger, raiser
from ..meta import obj

ls = ["logger", "raiser"]

def create(args):
    module = {
        _: globals()[_].create(args) for _ in ls
    }
    return obj(module)

all = [
    "create"
]