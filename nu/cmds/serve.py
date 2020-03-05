import sys, os, subprocess
from pathlib import Path

def pythoncode(nupath='', **kwargs):
    mindpath = Path(os.path.join(nupath, Path('abstract/__serve__.py')))
    code = mindpath.read_text()
    return code

def cmd(_, args, **kwargs):
    serving_file = Path('__serve__.py')
    if not serving_file.exists():
        with serving_file.open('w') as server:
            server.write(pythoncode(**kwargs))
    subprocess.run(["env", "FLASK_APP=__serve__.py", "flask", "run"])
    os.remove(serving_file)