from pathlib import Path
from inspect import ismodule
import os

from .common import merge


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
            self.__validators__ = {}
            self.update(kwargs)

        def __contains__(self, key, no_builtins=False):
            if super().__contains__(key): return True
            elif key in self['__builtins__'] and not no_builtins: return True
            # elif key in __module__ ???
            return False

        def __getitem__(self, key):
            if super().__contains__(key):
                return super().__getitem__(key)
            elif key in self['__builtins__']:
                return dict.__getitem__(self, '__builtins__')[key]
            # elif key in __module__ ???
            else: return SymboleInstance(key)

        def __fs_scan__(self, d, kls, FIRST=True):
            body = {}
            if FIRST:
                if 'ENTITY_PATH' in kls.__dict__:
                    d = Path(kls.ENTITY_PATH).resolve().absolute()
                if 'SHADOW_PATH' in kls.__dict__:
                    shadow_body = self.__fs_scan__(Path(kls.SHADOW_PATH).resolve().absolute(), type(None))
                    body = merge(body, shadow_body)
            assert d.exists(), "Entity " + str(d) + ' does not exists'
            assert d.is_dir(), "Can't scan " + str(d) + ", it's not a folder"
            body['__home__'] = d
            for l in os.listdir(d):
                if l.startswith('__') or l.endswith('__'):
                    continue
                elif os.path.isdir(Path(d, l)):
                    if l == '.entity':
                        res = self.__fs_scan__(Path(d, l), kls, FIRST=False)
                        if '__entity__' in body.keys():
                            body['__entity__'] = merge(res, body['__entity__'])
                        else:
                            body['__entity__'] = res
                    elif not l.startswith('.') and not ('-' in l):
                        res = self.__fs_scan__(Path(d, l), type(None), FIRST=False)
                        if '__' + str(l) in body.keys():
                            body['__' + str(l)] = merge(res, body['__' + str(l)])
                        else:
                            body['__' + str(l)] = res
                else:
                    body[l.replace('.', '_')] = Path(d, l).resolve().absolute()
            return body

        def __setitem__(self, key, value):
            #print ("SET\t\t", key, value, "\t\t", hasattr(value, '__name__'))
            if hasattr(value, '__name__'):
                if isinstance(value, type): # Awake fs-entity
                    d = Path(key).resolve().absolute()
                    if 'NO_ENTITY' in value.__dict__ and value.NO_ENTITY == True:
                        dict.__setitem__(self, key, value)
                    elif 'ENTITY_DATA' in value.__dict__:
                        if 'SHADOW_PATH' in value.__dict__:
                            shadow_body = self.__fs_scan__(Path(value.SHADOW_PATH).resolve().absolute(), type(None))
                            dict.__setitem__(self, key, EntityInstance(value, **merge(value.ENTITY_DATA, shadow_body)))
                        else:
                            dict.__setitem__(self, key, EntityInstance(value, **value.ENTITY_DATA))
                    else:
                        body = self.__fs_scan__(d, value)
                        dict.__setitem__(self, key, EntityInstance(value, **body))
                elif not key in self.__validators__.keys() and hasattr(value, '__call__'): # Add a validator
                    self.__validators__[key] = value
                elif ismodule(value):
                    dict.__setitem__(self, key, value)
                elif key in self.__validators__.keys(): # use validator
                    test = self.__validators__[key](value)
                    if not (test is None):
                        dict.__setitem__(self, key, test)
                else:
                        print ('Unknow: ', key, type(value))
                        exit()
            else:
                if key in self.__validators__.keys():
                    res = self.__validators__[key](value)
                    if res is None:
                        print ('Unable to set symbole: ', key)
                        exit()
                    else:
                        dict.__setitem__(self, key, res)
                        return
                print ('Unable to set symbole: ', key, ' no validator defined')
                exit()


class EntityInstance:
    class EntityScopeInstance(ScopeInstance):
        def __init__(self, entity, **kwargs):
                self.__entity__ = entity
                super().__init__(**kwargs)
                dict.__setitem__(self, 'exec', self.__entity__)
        class KwargEntityScopeInstance(ScopeInstance):
            def __init__(self, scope, **kwargs):
                self.__scope__ = scope
                super().__init__(**kwargs)
            def __contains__(self, key):
                if super().__contains__(key, no_builtins=True): return True
                else: return self.__scope__.__contains__(key)
            def __getitem__(self, key):
                if super().__contains__(key, no_builtins=True):
                    return super().__getitem__(key)
                else:
                    return self.__scope__.__getitem__(key)
            def __setitem__(self, key, value):
                if super().__contains__(key, no_builtins=True): return super().__setitem__(key, value)
                else: return self.__scope__.__setitem__(key, value)
    def __init__(self, *args, **kwargs):
        self.__dict__ = self.__class__.EntityScopeInstance(self, **kwargs)
        if '__entity__' in self.__dict__:
            orders = sorted(self.__dict__['__entity__'].keys())
            name = "\t"
            if '__home__' in self.__dict__:
                name = os.path.split(str(self.__home__))[-1]
            for k in orders:
                if k.startswith('__'): continue
                if k.endswith('_py'):
                    print (name, '\t\t', k)
                    self.__exec__(self.__entity__[k].read_text())

    def __exec__(self, code, **kwargs):
        try:
            if len(kwargs.keys()) > 0:
                exec(code, self.__dict__.KwargEntityScopeInstance(self.__dict__, **kwargs))
            else:
                exec(code, self.__dict__)
        except Exception as er:
            print ('Raised when executing code: \n', code)
            print (er)
            # ERROR HHANDLING
            if False:
                r = input('?: ')
                if 'raise' in r:
                    raise er
                elif 'exit' in r:
                    exit()
            else:
                raise er
            # ERROR HHANDLING
    def __call__(self, *args, **kwargs):
        if (not isinstance(args[0], Path)) and len(args) == 1 and len(kwargs) == 0: # FUNCTION decoration
            fun = args[0]
            assert not fun.__name__ in self.__dict__, f"Function {fun.__name__} already defined in {repr(self)}"
            self.__dict__[fun.__name__] = fun
            return
        for arg in args:
            if isinstance(arg, Path):
                self.__exec__(arg.read_text(), **kwargs)
            else:
                raise Exception('Unknow call args: ', (args, kwargs))
            #!