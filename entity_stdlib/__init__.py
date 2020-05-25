import sys, os
from pathlib import Path

STDLIB_PATH = Path(os.path.split(__file__)[0])

print (STDLIB_PATH)

scripts = {}
for f in os.listdir(STDLIB_PATH):
    if not f.startswith('__'):
        scripts[f.replace('.py', '')] = Path(STDLIB_PATH, f)


all = [
    'STDLIB_PATH', 'scripts'
]