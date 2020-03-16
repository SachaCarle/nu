import sys, os, subprocess
import argparse

#Assert babel installation
subprocess.run(["npm", "install", ], shell=True)
# Done

parser = argparse.ArgumentParser()
parser.add_argument('target', help="target file")

args = parser.parse_args()

from .env import ExecuteJs

ExecuteJs(fd=args.target)