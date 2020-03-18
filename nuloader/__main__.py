from . import nupath
import os, sys, subprocess


os.environ['PYTHONPATH'] = nupath
try:
    idx = sys.argv.index('--')
    args = sys.argv[idx:]
except:
    idx = -1
    args = []
subprocess.run(["python", '-m', "nu", *args])