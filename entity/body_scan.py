from pathlib import Path
import os, sys
from os import listdir
from os.path import isfile

def fs_scan(path, **others):
    bd = {
        'body_path': str(Path(path).resolve().absolute())
    } # BODY DATA
    fs = listdir(path)
    if '.entity' in fs:
        mind_path = Path(path, '.entity')
        mind_fs = listdir(mind_path)
        for k in mind_fs:
            mfpath = Path(mind_path, k)
            if k == "mind.py":
                bd['mind'] = mfpath
            elif k.endswith('.py') and isfile(mfpath):
                bd['_' + k.replace('.py', '_')] = mfpath
            else:
                print ('ignored: ', mfpath)
            for name, value in others.items():
                if value[0] in (True, 'mind') and k.endswith('.' + name) and isfile(mfpath):
                    bd[value[1].format(k.replace('.' + name, ''), 'mind')] = mfpath
    for k in fs:
        mfpath = Path(path, k)
        if isfile(mfpath) and k.endswith('.py'):
            bd[k.replace('.py', '')] = mfpath
        for name, value in others.items():
            if value[0] in (True, 'body') and k.endswith('.' + name) and isfile(mfpath):
                bd[value[1].format(k.replace('.' + name, ''), 'body')] = mfpath
    return bd
