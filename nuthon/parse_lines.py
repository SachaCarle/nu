from . import FreeParser, LETTERS

def _separate_lines(s):
    res = s.split('\n')
    return res

def _separate_comments(s):
    res = {}
    state = False
    lines = _separate_lines(s)
    for l in lines:
        if l.startswith('#'):
            if l.startswith('# OPEN '):
                s = l.replace('# OPEN ', '')
                res[s] = []
                assert state is False
                state = s
            elif l.startswith('# CLOSE '):
                s = l.replace('# CLOSE ', '')
                assert state != False
                state = False
            else:
                print ("~", l)
        elif state != False:
            res[state].append(l)
        else:
            pass
    return res

class parse_lines(FreeParser):
    def __init__(self, sym_str):
        FreeParser.__init__(self, sym_str, _separate_comments)