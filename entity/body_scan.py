from pathlib import Path
import os, sys
from os import listdir
from os.path import isfile

def fs_scan(path):
    bd = {

    } # BODY DATA
    fs = listdir(path)
    print (fs)
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
        for k in fs:
            mfpath = Path(path, k)
            if isfile(mfpath) and k.endswith('.py'):
                bd[k.replace('.py', '')] = mfpath
        return bd
