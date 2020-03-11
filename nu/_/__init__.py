from . import logger, raiser, parser
from ..meta import obj

ls = ["logger", "raiser", "parser"]

def create(args):
    module = {
        _: globals()[_].create(args) for _ in ls
    }
    return obj(module)

all = [
    "create"
]