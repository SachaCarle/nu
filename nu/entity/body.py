from string import Template
import webbrowser, json, shutil, os, nu
from pathlib import Path

def move(e):
    def _move(loc):
        folder = os.path.split(e.location)
        folder = folder[0]
        dady = os.path.split(folder)
        nl = dady[1]
        dady = dady[0]
        b = Path(loc, nl).resolve()
        nu.moved(e, b) # CODE END
    return _move

def duplicate(e):
    def _dupl():
        folder = os.path.split(e.location)
        folder = folder[0]
        dady = os.path.split(folder)
        nl = dady[1]
        dady = dady[0]
        b = Path(dady, nl, nl).resolve()
        try:
            nu.duplicate(e, b)
        except Exception as er:
            e.think("I can't create a clone, ", str(er).encode('ascii', 'replace'))
    return _dupl

def opt(e):
    d = {}
    if 'analyze' in e:
        #d['analyze_tokens'] = json.dumps(e.analyze['tokens']).replace('\\"', "'").replace("\\r", "__backslash__r").replace("\\n", "__backslash__n")
        d['analyze_tokens'] = str(e.analyze['tokens'])
    return d

def bodyset(e):
    def _set(txt):
        adding = opt(e)
        txt = Template(txt).safe_substitute(**e, **adding)
        e.body.file.write_text(txt)
    return _set

def show(e):
    def _instanciate():
        webbrowser.open(e.http + str(e.body.file))
    return _instanciate