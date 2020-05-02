from entity import Entity
from pathlib import Path
import sys, os, argparse

parser = argparse.ArgumentParser(description='Awaken on or more Entity.')
parser.add_argument('ets', metavar='E', type=str, nargs='+',
                    help='Folder containing an Entity.')

res = parser.parse_args(sys.argv)

from .body_scan import fs_scan

for k in res.ets:
    if k != __file__:
        print ("Awekening: ", k)
        fs = fs_scan(k)
        e = Entity(
            **fs
        )

# LOAD AN ENTITY BY FILE SYSTEM !!

#!