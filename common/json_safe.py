from common import AbstractNamespace
from pathlib import Path

def json_safe_dict(dd):
    if isinstance(dd, (str, Path)):
        return str(dd)
    return {
        k: v if not isinstance(dd, (dict, AbstractNamespace))
            else json_safe_dict(v)
        for k, v in (dd.items() if isinstance(dd, dict) else dd('items'))
    }
