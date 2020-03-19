from string import Template
import webbrowser, json

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
        e.body.file.touch()
        e.body.file.write_text(txt)
    return _set

def show(e):
    def _instanciate():
        webbrowser.open(e.http + str(e.body.file))
    return _instanciate