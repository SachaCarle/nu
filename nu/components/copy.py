import sys, os, subprocess, nu
from pathlib import Path

module_path = Path(os.path.split(__file__)[0]).resolve()

def copy(cp_name, entity):
    cp_file_js = Path(module_path, cp_name + '.js')
    cp_file_map = Path(module_path, cp_name + '.js.map')
    if not cp_file_js.exists():
        raise Exception(str(cp_file_js) + ' does not exist')
    if not cp_file_map.exists():
        raise Exception(str(cp_file_js) + ' does not exist')
    cp_entity = Path(entity.location, cp_name + '.js').resolve()
    cp_entity_map = Path(entity.location, cp_name + '.js.map').resolve()
    with cp_entity.open('w') as fd:
        fd.write(cp_file_js.read_text())
    with cp_entity_map.open('w') as fd:
        fd.write(cp_file_map.read_text())
