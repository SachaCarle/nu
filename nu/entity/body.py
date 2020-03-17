from string import Template
import webbrowser

def bodyset(e):
    def _set(txt):
        txt = Template(txt).safe_substitute(**e)
        e.body.file.touch()
        e.body.file.write_text(txt)
    return _set

def show(e):
    def _instanciate():
        webbrowser.open(e.http + str(e.body.file))
    return _instanciate