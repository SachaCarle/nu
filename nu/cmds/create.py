import os.path
import shutil, subprocess
import json, nu
from pathlib import Path

def pythoncode():
    mindpath = Path(os.path.join(nu.nupath, Path('abstract/mind.py')))
    code = mindpath.read_text()
    return code

def cmd(_, args, legacy=True, **kwargs):
    default_attr = {
        'components': {'data':[]}
    }
    assert args.o
    name = args.o
    entity_name = os.path.split(args.o)[1]
    assert name
    entity_path = Path(name + '.nu').resolve()
    folder_path = Path(os.path.join(name + '.nu', '.entity')).resolve()
    try:
        folder_path.mkdir(parents=True, exist_ok=True)
        _.logger('creating at ', folder_path)
        entityfile = Path(os.path.join(folder_path, 'entity.json')).resolve()
        tx = json.dumps({'name': entity_name, 'home': str(folder_path), 'default_body': 'body.html', **default_attr})
        with entityfile.open('w') as entity:
            entity.write(tx)

        mindfile = Path(os.path.join(folder_path, 'mind.py'))
        with mindfile.open('w') as mind:
            mind.write(pythoncode())
    except Exception as e:
        if legacy:
            shutil.rmtree(entity_path)
            _.logger('cleaned ', entity_path)
        raise e
