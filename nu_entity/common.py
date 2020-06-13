import os, pathlib

def merge(source, destination):
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge(value, node)
        else:
            destination[key] = value

    return destination


def dict_walk(d):
    for k in d.keys():
        if isinstance(d[k], dict):
            for kk in dict_walk(d[k]):
                yield (k, *kk)
        else:
            yield (k, )

def dict_chain_get(d, chain):
    for k in chain:
        if not (k in d.keys()):
            return None
        d = d[k]
    return d

def dict_chain_set(d, chain, value):
    for k in chain[:-1]:
        if not k in d.keys():
            d[k] = {}
        d = d[k]
    d[chain[-1]] = value

def fs_scan(p):
    body = {}
    for k in os.listdir(p):
        np = pathlib.Path(p, k)
        if np.is_dir():
            if k.endswith('.entity') or (not k.startswith('.')):
                body[k] = fs_scan(np)
        else:
            body[k] = np
    return body
def merge_paths(a, b):
    # first with b
    body_b = fs_scan(b)
    body_a = fs_scan(a)
    for k in dict_walk(body_b):
        presence = dict_chain_get(body_a, k)
        if presence is None:
            dict_chain_set(body_a, k, dict_chain_get(body_b, k))
    return body_a
