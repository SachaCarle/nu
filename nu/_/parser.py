from pathlib import Path
import ast, pprint



pp = pprint.PrettyPrinter(indent=4)

class IndentationFeedback(Exception):
    def __init__(self, *args):
        Exception.__init__(self)
        self.args = args

def indent_mesure(l, indent, indent_type='    '):
    _indent = indent
    i = 0
    try:
        while _indent > 0:
            if l[0:len(indent_type)] != indent_type:
                raise IndentationFeedback(l[0:len(indent_type)])
            l = l[len(indent_type):]
            _indent -= 1
        i += 1
    except IndentationFeedback:
        return False
    return True

class ScopeItem:

    def close_block(self, line):
        self.block_stack.close()
        self.block_stack = None
        return self.add_line(line)

    def add_line(self, line):
        if line == '': return
        if self.block_stack != None:
            return self.block_stack.add_line(line)
        else:
            try:
                res = parse_line(line, indent=self.indent, parent=self)
            except IndentationFeedback as ie:
                if self.block_stack != None:
                    self.block_stack.close()
                    self.block_stack = None
                    return self.add_line(line)
                elif self.parent != None:
                    return self.parent.close_block(line)
                else:
                    print ('Indentation Feedback Error ====> ', ie.args, '\n\t', str(self), '\n', self.parent != None)
                    raise ie
            else:
                #print (self.head(), 'GOT', res)
                if res['typ'] == "ast":
                    self.lines[self.count] = (res['a'], line)
                    self.count += 1
                elif res['typ'] == "block":
                    assert self.block_stack == None
                    self.lines[self.count] = res['b']
                    self.count += 1
                    self.block_stack = res['b']
                    pass
        return True

    def close(self):
        #print ('\tFINISHED !!', self.lines)
        pass

    def __init__(self, code=None, parent=None, bt=None, tks=(), indent=0):
        self.count = 0
        self.lines = {}
        self.block_stack = None
        self.parent = parent
        self.builtin_type = bt
        self.tokens = tks
        self.indent = indent
        if code:
            for l in code.split('\n'):
                self.add_line(l)

    def __str__(self):
        return str([self.indent, self.builtin_type, *self.tokens, 'LINES', self.lines])

    def __repr__(self):
        return str(self)

    def head(self):
        s = (self.indent - 1) * '    '
        if self.builtin_type != None:
            s += self.builtin_type + ' ' + ' '.join(self.tokens)
        else:
            s +=  ' '.join(self.tokens)
        return s

    def __call__(self, *args):
        return '\n'.join([ l[1] if isinstance(l, tuple) else hel(l) for i,l in self.lines.items()])

def hel(sc):
    res = sc('python')
    if sc.builtin_type != None:
        return sc.head() + '\n' + res
    return '<U_SCOPE' + str(sc.indent) + ' ' + str(sc.tokens)+ ' >' + str(res) + '</U_SCOPE>'

def parse_block(l, indent, parent):
    tks = l.split(' ')
    if len(tks) == 1:
        tks = [tks[0][0:-1], ':']
    if tks[0] in ('def', 'if', 'elif', 'else', 'for', 'while', 'class', 'try', 'except', 'finally'):
        builtin = tks[0]
        return ScopeItem(indent=indent + 1, parent=parent, bt=builtin, tks=tks[1:])
    return ScopeItem(indent=indent + 1, parent=parent, tks=tks)

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
    try:
        if l.endswith(':'):
            typ = 'block'
            b = ast.parse(l)
        else:
            typ = 'ast'
            a = ast.parse(l)
    except SyntaxError as e:
        if l.endswith(':'):
            typ = 'block'
            b = parse_block(l, indent, parent)
    return { 'typ': typ, 'a': a, 'b': b}

def pythoncode(loc):
    mindpath = Path(loc)
    code = mindpath.read_text()
    return code

def create(args):
    def parser(filep):
        code = pythoncode(filep)
        scope = ScopeItem(code)
        return scope
    return parser