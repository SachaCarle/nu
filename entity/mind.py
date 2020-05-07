class Mind(dict):
    MIND_KEY = 'mind'
    def __call__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], str):
            code = self.body[args[0]]
            exec(code, {
                self.MIND_KEY: self, **self, **kwargs
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
        for k in self.body.keys():
            if k.startswith('_') and k.endswith('_'):
                self(k)
        if self.MIND_KEY in self.body.keys():
            self(self.MIND_KEY)
