class ___:
    def __getattribute__(self, key):
        pass
    def __setattr__(self, key, value):
        pass
    def __delattr__(self, key):
        pass
class Mind(dict):
    def __call__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], str):
            code = self.body[args[0]]
            exec(code, {
                'mind': self, **self, **kwargs
            })
            return self.me
        elif len(args) == 1 and not isinstance(args[0], (int, dict, tuple, list)):
            fun = args[0]
            res = fun(self, fun)
            if res != None:
                self[fun.__name__] = res
            return self.me
        else:
            assert False

    def __init__(self, entity, body):
        self.body = body
        self.me = entity
        if 'mind' in self.body.keys():
            self('mind')
