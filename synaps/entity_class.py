from common import AbstractNamespace
from abstract import AbstractException
from functools import partial


class Entity(dict):
    def_attrs = {
        'name': 'entity',
        'body_state': 'abstract',
        'head_state': 'abstract',
        'body': {

        },
        'head': {
            'mind': f"""
print ('lol')
print (locals().keys())
think('Awakened!')
""",
        }
    }
    def __init__(self, synaps):
        self.synaps = synaps
        self.name = 'UnknowEntity' if not 'name' in self.def_attrs else self.def_attrs['body_state']
        self.funs = {}
        body_location, head_location = self.synaps.getEntityLocation(self)
        self.body = AbstractNamespace('body', parent=body_location, state=self.def_attrs['body_state'])
        self.head = AbstractNamespace('head', parent=head_location, state=self.def_attrs['head_state'])
        for k, v in self.def_attrs['body'].items():
            setattr(self.body, k, v)
        for k, v in self.def_attrs['head'].items():
            setattr(self.head, k, v)

    def __getattr__(self, key):
        if key in self.head:
            return getattr(self.head, key)
        return None

    def __call__(self, *args, **kwargs):
        code = None
        if len(args) == 0 and len(kwargs) == 0:
            code = self.head.mind
        elif len(args) == 1 and len(kwargs) == 0:
            if isinstance(args[0], str):
                assert False
            else:
                # get fun :)
                fun = args[0]
                self.funs[fun.__name__] = partial(fun, self)
                return
        elif len(args) > 0:
            if isinstance(args[0], str):
                assert False
            else:
                return self.funs[args[0]](*args[1:], **kwargs)
        if code == None:
            raise AbstractException("Unknow call: ", args, kwargs)
        exec(code, {**self.funs})


