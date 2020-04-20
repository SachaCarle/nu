from common import AbstractNamespace
from abstract import AbstractException
from functools import partial
from sys import stdout


class Entity(dict):
    def_attrs = {
        'name': 'entity',
        'body_state': 'physical',
        'head_state': 'abstract',
        'body': {

        },
        'head': {
            'mind': f"""
think('Awakened!')
""",
        }
    }
    def __init__(self, synaps, *args, **kwargs):
        self.def_attrs = self.def_attrs.copy()
        self.def_attrs.update(kwargs)
        self.synaps = synaps
        self.name = 'UnknowEntity' if not 'name' in self.def_attrs else self.def_attrs['name']
        self.uri = "/" + self.__class__.__name__ + '/' + str(id(self))
        self.funs = {}
        body_location, head_location = self.synaps.getEntityLocation(self)
        self.body = AbstractNamespace('body', parent=body_location, state=self.def_attrs['body_state'])
        self.head = AbstractNamespace('head', parent=head_location, state=self.def_attrs['head_state'])
        for k, v in self.def_attrs['body'].items():
            setattr(self.body, k, v)
        for k, v in self.def_attrs['head'].items():
            setattr(self.head, k, v)
        @self
        def think(self, *args):
            stdout.write (self.name + ':' + ', '.join([str(_) for _ in args]) + '\n')
            stdout.flush()

    def __getitem__(self, k, *args):
        if isinstance(k, (tuple, list)):
            return self.__getitem__(k[0], *k[1:])
        kk = 'html_' + k
        try:
            r = getattr(self, kk)
        except Exception as e:
            return Entity.__getitem__(self, k, *args)
        return r(*args)

    def __getattr__(self, key):
        if key in self.head:
            return getattr(self.head, key)
        return None

    def __call__(self, *args, **kwargs):
        code = None
        if len(args) == 0 and len(kwargs) == 0:
            code = self.head.mind
        elif (not isinstance(args[0], str)) and len(args) == 1 and len(kwargs) == 0:
            fun = args[0]
            self.funs[fun.__name__] = partial(fun, self)
            return self.funs[fun.__name__] # FUN
        elif len(args) > 0:
            if isinstance(args[0], str):
                return self.funs[args[0]](*args[1:], **kwargs)
            else:
                assert False, (args,  kwargs)
        if code == None:
            raise AbstractException("Unknow call: ", args, kwargs)
        try:
            exec(code, {'_': self, **self.funs, **self})
        except Exception as er:
            print ("Entity Failed: " + str(self))
            raise er

    def __repr__(self):
        return "<" + self.name + ': ' + str(self.keys()) + ">"
    def __str__(self):
        return "<" + self.name + ': ' + dict.__str__(self) + ">"

    def html_short(self):
        return f"""<div><a style='font-size: large;' href={self.uri}>{self.name}<a><code>{
            dict.__str__(self)
        }</code></div>"""



#!