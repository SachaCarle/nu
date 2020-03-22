import sys, os, subprocess, shutil, nu
from pathlib import Path

class Access:
    def __init__(self, di):
        self.di = str(Path(
            di
        ).resolve())
    def __enter__(self):
        self.oldcwd = os.getcwd()
        print (self.oldcwd, " > ", self.di)
        os.chdir(self.di)
        return self.di
    def __exit__(self, type, value, traceback):
        #Exception handling here
        os.chdir(self.oldcwd)
        print (self.di, " > ", self.oldcwd)

def moved(entity, destination, **pray):
    old = os.path.split(entity.location)[0]
    entity.think('I will ask father to move me.', old, destination)
    entity.pray("move", old, str(destination), **pray)
    entity.think('I will sleep now...')
    exit()

def duplicate(entity, destination):
    old = os.path.split(entity.location)[0]
    shutil.copytree(old, str(destination))
    def _awaken_():
        with Access(destination):
            entity.think('Where did my mind wonder ??', os.getcwd())
            return nu.cmds.awake.awaken()
    return _awaken_
