from pathlib import Path
from .Entity import Entity
from common import remkdir
import os, json

default_attrs = {
    'head': 'mind.py'
}

def load(name):
    fp = Path(os.path.join(name, 'entity.json'))
    if fp.exists():
        with fp.open('r') as f:
            return Entity(def_attrs=json.load(f))
    raise Exception(ef, ": does not exists...")

def create(name):
    remkdir(name)
    return Entity(name, def_attrs=default_attrs)