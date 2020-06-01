
from pathlib import Path
import sys, os, argparse
from . import ScopeInstance


parser = argparse.ArgumentParser(description='Awaken on or more Entity.')
parser.add_argument('ets', metavar='E', type=str, nargs='+',
                    help='Folder containing an Entity.')
parser.add_argument('--silent', help='Will not output awakening info', action='store_true')
parser.add_argument('-x', help='execute code on the global scope')

res = parser.parse_args(sys.argv)

global_scope = ScopeInstance()
for k in res.ets:
    if k != __file__:
        if not res.silent:
            print ("Awakening: ", k)
        class fake:
            __name__ = k
        global_scope[k] = fake

if res.x:
    exec (res.x, global_scope)