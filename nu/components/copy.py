import sys, os, subprocess, nu
from pathlib import Path

module_path = Path(os.path.split(__file__)[0]).resolve()
components_path = Path(module_path, 'builded')

def copy(cp_name, entity):
    cp_file_js = Path(module_path, cp_name + '.js')
    cp_file = Path(components_path, cp_name)
    if not cp_file_js.exists():
        raise Exception(str(cp_file_js) + ' does not exist')
    print (cp_file_js, cp_file)