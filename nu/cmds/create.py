import os.path
import shutil, subprocess
from pathlib import Path

def pythoncode():
    mindpath = Path(os.path.join(Path('.').resolve(), Path('nu/abstract/mind.py')))
    code = mindpath.read_text()
    return code

def cmd(_, args, legacy=True):
    name = args.o
    assert name
    folder_path = Path(name + '.nu').resolve()
    try:
        folder_path.mkdir()
        _.logger('creating at ', folder_path)
        mindfile = Path(os.path.join(folder_path, 'mind.py'))
        with mindfile.open('w', ) as mind:
            mind.write(pythoncode())
        subprocess.run(["python", str(mindfile)], cwd=str(folder_path))
    except Exception as e:
        if legacy:
            shutil.rmtree(folder_path)
            _.logger('cleaned ', folder_path)
            cmd(_, args, False)
        else:
            raise e
