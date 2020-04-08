import os

class AbstractNamespace(object):
    def __call__(self, *args, **kwargs):
        if args[0] == 'abstract':
            return object.__getattribute__(self, 'datas')
        if args[0] == 'physical':
            return object.__getattribute__(self, 'fs')
        if args[0] == 'ari':
            return object.__getattribute__(self, 'interface')
        if args[0] == 'state':
            if len(args) == 1:
                return object.__getattribute__(self, 'state')
            elif args[1] in ['physical', 'abstract', 'ari']:
                old = self('state')
                return AbstractNamespace.__init__(self, object.__getattribute__(self, 'name'),
                    state=args[1], **{old: self(old)})
                object.__setattr__(self, 'state', 'physical')
        raise Exception('unknow call: ' + str(args) + "\nalso\t" + str(kwargs))

    def __remap__(self, d):
        for key, value in d.items():
            if isinstance(value, AbstractNamespace):
                subname = object.__getattribute__(value, 'name')
                print ('!!', key, value, subname)
                value('state', self('state'))
                print ('-->', key, value, subname)
            setattr(self, key, value)

    def __init__(self, name, state='abstract', abstract=False, physical=False, ari=False):
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'state', state)
        if self('state') == 'abstract':
            object.__setattr__(self, 'datas', dict() if not abstract else abstract)
        elif self('state') == 'physical':
            object.__setattr__(self, 'fs', dict() if not physical else physical)
            if not (abstract is False):
                self.__remap__(abstract)

    def __getattribute__(self, key):
        if key.startswith('__'):
            return object.__getattribute__(self, key)
        else:
            if self('state') == 'abstract':
                return object.__getattribute__(self, 'datas')[key]
            if self('state') == 'physical':
                return object.__getattribute__(self, 'fs')[key]

    def __setattr__(self, key, value):
        if key.startswith('__'):
            raise Exception('Can\'t alter ' + key)
        else:
            if self('state') == 'abstract':
                object.__getattribute__(self, 'datas')[key] = value
            if self('state') == 'physical':
                fs = self('physical')
                if key in fs.keys():
                    pass# open and re-write
                else:
                    pass# open and write
                # DEBUG
                fs[key] = value

    def __str__(self):
        if self('state') == 'abstract':
            return f"[{object.__getattribute__(self, 'name')}({self('state')}): {str(object.__getattribute__(self, 'datas'))}]"
        elif self('state') == 'physical':
            return f"[{object.__getattribute__(self, 'name')}({self('state')}): {str(list(object.__getattribute__(self, 'fs').keys()))}]"

    def __repr__(self):
        if self('state') == 'abstract':
            return f"[{object.__getattribute__(self, 'name')}({self('state')}): {str(list(object.__getattribute__(self, 'datas').keys()))}]"
        elif self('state') == 'physical':
            return f"[{object.__getattribute__(self, 'name')}({self('state')}): {str(list(object.__getattribute__(self, 'fs').keys()))}]"