class CallInstance(list):
    def __repr__(self):
        return f"<Call {self}>"
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
    def __str__(self):
        more = ', '.join(f"{k}={v}" for k, v in self.kwargs.items())
        return f"({', '.join(str(it) for it in self.args)}{', ' if more != '' else ''}{more})"
    def __getattr__(self, key):
        return self.ExpressionInstance(self, '.', key)
    def __call__(self, *args, **kwargs):
        return ExpressionInstance(self, CallInstance(*args, **kwargs))

class ExpressionInstance(list):
    def __repr__(self):
        return f"<Expression {self}>"
    def __init__(self, *args):
        self.args = args
    def __str__(self):
        return f"{''.join(str(it) for it in self.args)}"
    def __getattr__(self, key):
        return self.__class__(self, '.', key)
    def __call__(self, *args, **kwargs):
        return ExpressionInstance(self, CallInstance(*args, **kwargs))

class SymboleInstance(str):
    def __repr__(self):
        return f"<Symbole {super().__repr__()}>"
    def __getattr__(self, key):
        return ExpressionInstance(self, '.', key)
    def __call__(self, *args, **kwargs):
        return ExpressionInstance(self, CallInstance(*args, **kwargs))

class ScopeInstance(dict):
        def __init__(self, **kwargs):
            dict.__init__(self)
            dict.__setitem__(self, '__builtins__', __builtins__)
            self.update(kwargs)

        def __contains__(self, key):
            if super().__contains__(key): return True
            elif key in self['__builtins__']: return True
            # elif key in __module__ ???
            return False

        def __getitem__(self, key):
            if super().__contains__(key):
                return super().__getitem__(key)
            elif key in self['__builtins__']: return dict.__getitem__(self, '__builtins__')[key]
            # elif key in __module__ ???
            else: return SymboleInstance(key)

        def __setitem__(self, key, value):
            raise Exception('Unable to set symbole: ', key)




            #!