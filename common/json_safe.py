from common import AbstractNamespace
from pathlib import Path
import json

#Entity = None

def json_safe_dict(dd):
    if dd.__class__.__name__ == "Entity":
        return "<entity>"
    if isinstance(dd, (str, Path, int)):
        return str(dd)
    if isinstance(dd, (list,)):
        return json.dumps(dd)
    return {
        k: v if not isinstance(dd, (dict, AbstractNamespace))
            else json_safe_dict(v)
        for k, v in (dd.items() if isinstance(dd, dict) else dd('items'))
    }
