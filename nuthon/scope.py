from .indentation import IndentationFeedback

def hel(sc):
    res = sc()
    if sc.builtin_type != None:
        return sc.head() + '\n' + res
    if sc.is_extension:
        return res
    return '<U_SCOPE' + str(sc.indent) + ' ' + str(sc.tokens)+ ' >' + str(res) + '</U_SCOPE>'


class ScopeItem:
    is_extension = False

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
                res = self.parse_line(line, indent=self.indent, parent=self)
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

    def __init__(self, parse_line, code=None, parent=None, bt=None, tks=(), indent=0):
        self.count = 0
        self.lines = {}
        self.block_stack = None
        self.parent = parent
        self.builtin_type = bt
        self.tokens = tks
        self.indent = indent
        self.parse_line = parse_line
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
