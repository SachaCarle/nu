class FreeParser:
    def __init__(self, sym_str, separator):
        self.sym_str = sym_str
        self.res = separator(self.sym_str)

    def __str__(self):
        return str(self.res)
    def __repr__(self):
        return '<' + self.sym_str + '>'