from .grammar_ext import GrammarExt, hel
import ast
from ast import Expr

def _getNone(*args, **kwargs):
    return None

class NuBlock(GrammarExt):
    implementation_format = "__nuthon__({key}, {body}, {expr})"

    @classmethod
    def from_str(cls, tks, parent=None):
        assert tks[1] == ':'
        jn = ast.parse(tks[0])
        assert isinstance(jn.body[0], Expr), str(jn.body.__class__) + ' is not an instance of ' + str(Expr)
        return True

    def formated(self, line_join=', ', expr_transform=_getNone):
        return {
            'key': self.tokens[0],
            'body': line_join.join(_[1] if isinstance(_, tuple) else _() for _ in self.lines.values()),
            'expr': expr_transform(self.tokens[1:])
            }

    def __call__(self, *args):
        return self.implementation_format.format(**self.formated())

    #def __call__(self, *args):
    #    return self.tokens[0] + '(' + ', '.join([l[1].strip() if isinstance(l, tuple) else hel(l) for i,l in self.lines.items()]) + ')'



GrammarExt.register(NuBlock)