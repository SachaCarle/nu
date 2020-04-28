from .composed_symbole_class import ComposedSymbole

class Symbole(str):
    __symboles__ = {}
    __composed__ = {}

    def __new__(kls, s, parent=None):
        if s in Symbole.__symboles__:
            return Symbole.__symboles__[s]
        else:
            r = str.__new__(kls, s)
            Symbole.__symboles__[s] = r
        return r

    def __init__(self, s):
        str.__init__(self)

    def __getattribute__(self, key):
        if key.startswith('__') and key.endswith('__'):
            return str.__getattribute__(self, key)
        if not key in Symbole.__symboles__:
            raise Exception("Symbole: " + key + ' is not defined.')
        return Symbole(key).__get__(self, Symbole)

    def __get__(self, key, kls):
        if kls == Symbole:
            return ComposedSymbole(Symbole(key), self)
        assert False


        #!