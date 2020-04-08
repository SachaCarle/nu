from pathlib import Path
from .Entity import Entity
from common import remkdir
import os, json

default_attrs = {
    'head': "me.think('default mind.. such waow!!')",
    'state': 'abstract',
}

def load(name):
    fp = Path(name, '.entity', 'entity.json')
    if fp.exists():
        with fp.open('r') as f:
            return Entity(def_attrs=json.load(f))
    raise Exception(fp, ": does not exists...")

def create(name):
    return Entity(name, def_attrs=default_attrs)