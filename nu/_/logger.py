def _nolog(*args, **kwargs):
    return

def _log(*args, **kwargs):
    return print(*args, **kwargs)

def create(args):
    if args.v == True:
        return _log;
    return _nolog;