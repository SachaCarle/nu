class Mind:
    def __getattribute__(self, key):
        pass
    def __setattr__(self, key, value):
        pass
    def __delattr__(self, key):
        pass
    def __call__(self, *args, **kwargs):
        if len(args) == 1 and not isinstance(args[0], (str, int, dict, tuple, list)):
            # fun !!
            fun = args[0]
            fun(self, me=fun)

    def __init__(self, entity, body):
        self.body = body
        self.me = entity
