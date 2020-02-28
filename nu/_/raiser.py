def _raise(name, *args, **kwargs):
    raise Exception(name, *args, kwargs)

def create(args):
    return _raise