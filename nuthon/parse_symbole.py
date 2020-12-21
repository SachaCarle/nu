from . import FreeParser

class parse_symbole:
    def __init__(self, sym_str):
        FreeParser.__init__(self)
        self.sym_str = sym_str
    def __str__(self):
        return self.sym_str