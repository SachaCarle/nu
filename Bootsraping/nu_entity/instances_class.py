from pathlib import Path


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

class EntityInstance:
    def __init__(self, *args, **kwargs):
        self.__dict__ = ScopeInstance(**kwargs)
    def __exec__(self, code):
        exec(code, self.__dict__)

class ScopeInstance(dict):
        def __init__(self, **kwargs):
            dict.__init__(self)
            dict.__setitem__(self, '__builtins__', __builtins__)
            self.__validators__ = {}
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

        def __fs_scan__(self, d, kls):
            assert d.exists(), "Entity " + str(d) + ' does not exists'
            body = {
                'home': d
            }
            return body

        def __setitem__(self, key, value):
            if hasattr(value, '__name__'):
                if isinstance(value, type):
                    d = Path(key).resolve().absolute()
                    body = self.__fs_scan__(d, value)
                    dict.__setitem__(self, key, EntityInstance(value, **body))
                if hasattr(value, '__call__'):
                    assert not key in self.__validators__.keys(), 'Validator already defined: ' + key
                    self.__validators__[key] = value
            else:
                if key in self.__validators__.keys():
                    res = self.__validators__[key](value)
                    if res is None:
                        raise Exception('Unable to set symbole: ', key)
                    else:
                        dict.__setitem__(self, key, res)
                        return
                raise Exception('Unable to set symbole: ', key, ' no validator defined')


            #!