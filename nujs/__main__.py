import sys, os, subprocess, json
from pathlib import Path
import argparse

#Assert babel installation
subprocess.run(["npm", "install", 'vue'])#, shell=True)
# Done

parser = argparse.ArgumentParser()
parser.add_argument('target', help="target file")
parser.add_argument('-i', help='input', default=False)
parser.add_argument('-o', help='output', default=False)


args = parser.parse_args()
stdin = False
stdout = False

if args.i:
    stdin = Path(os.path.join(Path('.').resolve(), Path(args.i)))
if args.o:
    stdout =Path(os.path.join(Path('.').resolve(), Path(args.o)))

from .env import ExecuteJs

if stdin:
    stdin = stdin.read_bytes()

js = ExecuteJs(fd=args.target, stdin=stdin)


if isinstance(js.result, Exception):
    print ('?', js.body)
    raise js.result
else:
    if not stdout:
        print ('?', js.result)


if stdout:
    with stdout.open('w') as fd:
        for it in js.result:
            if it != None:
                fd.write(json.dumps(it))