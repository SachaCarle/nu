from pathlib import Path
from .nuthon import ScopeItem, IndentationFeedback, GrammarExt
import ast, pprint



pp = pprint.PrettyPrinter(indent=4)

def parse_block(l, indent, parent):
    tks = l.split(' ')
    if len(tks) == 1:
        tks = [tks[0][0:-1], ':']
    if tks[0] in ('def', 'if', 'elif', 'else', 'for', 'while', 'class', 'try', 'except', 'finally'):
        builtin = tks[0]
        return ScopeItem(parse_line, indent=indent + 1, parent=parent, bt=builtin, tks=tks[1:])
    res = GrammarExt.infer(tks, parent=parent)
    if res:
        return res(parse_line, indent=indent + 1, parent=parent, tks=tks)
    return ScopeItem(parse_line, indent=indent + 1, parent=parent, tks=tks)

def parse_line(l, indent=0, parent=None, indent_type="    "):
    a = None
    b = None
    typ = 'error'
    _indent = indent
    while _indent > 0:
        if l[0:len(indent_type)] != indent_type:
            raise IndentationFeedback(l, l[0:len(indent_type)])
        l = l[len(indent_type):]
        _indent -= 1
    if l.endswith(':'):
        typ = 'block'
        try:
            b = ast.parse(l)
        except SyntaxError as e:
            b = parse_block(l, indent, parent)
    else:
        typ = 'ast'
        a = ast.parse(l)
    return { 'typ': typ, 'a': a, 'b': b}

def pythoncode(loc):
    mindpath = Path(loc)
    code = mindpath.read_text()
    return code

def create(args):
    def parser(filep):
        code = pythoncode(filep)
        scope = ScopeItem(parse_line, code=code)
        return scope
    return parser