from traceback import print_exc
import sys

class Mind(dict):
    MIND_KEY = 'mind'
    def __call__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], str):
            code = self.body[args[0]]
            try:
                exec(code, {self.MIND_KEY: self, **self, **kwargs})
            except Exception as err:
                print ('\n\tException during execution of script "' + str(args[0]) + '" on ' + repr(self.me))
                print_exc()
                exit()
            return self.me
        elif len(args) == 1 and not isinstance(args[0], (int, dict, tuple, list)):
            fun = args[0]
            res = fun(self.me)
            if res != None:
                self[fun.__name__] = res
            return self.me
        else:
            assert False

    def __setattr__(self, name, value):
        return object.__getattribute__(self, 'me').__setattr__(name, value)
    def __getattr__(self, name):
        if name in ['me']:
            return object.__getattribute__(self, 'me')
        return object.__getattribute__(self, 'me').__getattribute__(name)

    def __init__(self, entity, body):
        object.__setattr__(self, 'me', entity)
        self.body = body
        entity.__mind__ = self
        for k in self.body.keys():
            if k.startswith('_') and k.endswith('_'):
                self(k)
        if self.MIND_KEY in self.body.keys():
            self(self.MIND_KEY)
