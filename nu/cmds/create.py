import os.path
import shutil, subprocess
import json
from pathlib import Path

def pythoncode():
    mindpath = Path(os.path.join(Path('.').resolve(), Path('nu/abstract/mind.py')))
    code = mindpath.read_text()
    return code

def cmd(_, args, legacy=True, **kwargs):
    assert args.o
    name = args.o
    entity_name = os.path.split(args.o)[1]
    assert name
    folder_path = Path(name + '.nu').resolve()
    try:
        folder_path.mkdir()
        _.logger('creating at ', folder_path)
        entityfile = Path(os.path.join(folder_path, 'entity.json'))
        with entityfile.open('w') as entity:
            entity.write(json.dumps({'name': entity_name, 'default_body': 'body.html'}))

        mindfile = Path(os.path.join(folder_path, 'mind.py'))
        with mindfile.open('w') as mind:
            mind.write(pythoncode())
    except Exception as e:
        if legacy:
            shutil.rmtree(folder_path)
            _.logger('cleaned ', folder_path)
            cmd(_, args, False)
        else:
            raise e
