from pathlib import Path
import os, subprocess, shutil, sys
from time import sleep

def aprint(*args, **kwargs):
    print (*args, **kwargs)
    sys.stdout.flush()

def workship(s):
    aprint ("nugod hear : ", s)
    if s.startswith("'move' "):
        s = s.replace("'move' ", '')
        s = [_.replace("'", "") for _ in s.split(' ')]
        aprint ("nugod will move in 1 second: ", s)
        sleep(1)
        aprint ("nugod move: ", s)
        shutil.move(*s)

    """
        try:
            a = None
            b = None

            shutil.copytree(str(a), str(b))
                . move ??

        except Exception as er:
            e.think('can\'t move to', str(b), "\n\t", str(er))
"""