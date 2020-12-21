
from pathlib import Path
import sys, os, argparse
from . import ZoneScope


parser = argparse.ArgumentParser(description='Awaken on or more Entity.')
parser.add_argument('ets', metavar='E', type=str, nargs='+',
                    help='Folder containing an Entity.')
parser.add_argument('--silent', help='Will not output awakening info', action='store_true')
parser.add_argument('-x', help='execute code in the zone scope')

res = parser.parse_args(sys.argv)

global_scope = ZoneScope()
if not Path('.zone.nu').is_dir():
    raise Exception('Current directory is not a zone.')
if not res.silent:
    print ("Activating zone")

if res.x:
    exec (res.x, global_scope)