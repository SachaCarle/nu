from . import nupath
import os, sys, subprocess
from pathlib import Path

os.environ['PYTHONPATH'] = nupath
try:
    idx = sys.argv.index('--')
    args = sys.argv[idx+1:]
    #print (["python", '-m', "nu", *args])
except:
    idx = -1
    args = []
if len(sys.argv) <= 1:
    subprocess.run(["python", '-m', "nu", "daemon"])
    exit()
elif sys.argv[1].endswith('.nu.py'):
    subprocess.run(["python", *sys.argv[1:]])
    exit()
elif sys.argv[1].endswith('.py'):
    subprocess.run(["python", *sys.argv[1:]])
    exit()
subprocess.run(["python", '-m', "nu", *args])