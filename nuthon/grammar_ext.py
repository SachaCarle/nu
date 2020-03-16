from .scope import ScopeItem, hel

_exts = []

class GrammarExt(ScopeItem):
    is_extension = True

    @staticmethod
    def register(ext):
        _exts.append(ext)

    @staticmethod
    def infer(tks, parent=None):
        #print (tks)
        ress = []
        for ex in _exts:
            try:
                res = ex.from_str(tks)
            except Exception as e:
                print ('failed', ex.__name__, e)
                # inlog
            else:
                ress.append(ex)
        assert len(ress) != 0
        return ress[0]

    @classmethod
    def from_str(cls, tks, parent=None):
        return False