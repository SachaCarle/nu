import sys, os, subprocess

def cmd(_, args):
    subprocess.run(["env", "FLASK_APP=mind.py", "flask", "run"])