import sys, os, subprocess, nu
from pathlib import Path

def pythoncode(nupath='', **kwargs):
    mindpath = Path(os.path.join(nupath, Path('abstract/__awake__.py')))
    code = mindpath.read_text()
    return code

def awaken():
        try:
                spiritpath = Path(os.path.join('.entity', 'entity.json')).resolve()
                #print ('awakening', spiritpath)
                me = nu.entity.spirit(str(spiritpath))
        except Exception as e:
                print ("When trying to awaken", (spiritpath,), " an exception occured:")
                raise e
        else:
                me.think('A soft awakening, hello world !', os.getcwd())
                me.awake()
                return me

def cmd(_, args, **kwargs):
       return awaken()