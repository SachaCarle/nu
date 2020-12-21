from . import FreeParser, LETTERS

def _separate_symbole_in_string(s):
    res = []
    state = 'NONE'
    for i,c in enumerate(s):
        if c in LETTERS:
            if state == "NONE":
                res.append(c)
                state = "LETTERS"
            elif state == "LETTERS":
                res[-1] = res[-1] + c
            elif state == "OTHER":
                res.append(c)
                state = "LETTERS"
            else:
                assert False, state
        else:
            if state == "NONE":
                res.append(c)
                state = "OTHER"
            elif state == "LETTERS":
                res.append(c)
                state = "OTHER"
            elif state == "OTHER":
                res[-1] = res[-1] + c
            else:
                assert False, state
            pass
    return res



class parse_symbole(FreeParser):
    def __init__(self, sym_str):
        FreeParser.__init__(self, sym_str, _separate_symbole_in_string)

