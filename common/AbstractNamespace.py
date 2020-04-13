import os
from pathlib import Path

class AbstractNamespace(object):
    def __call__(self, *args, **kwargs):
        if args[0] == 'discover':
            assert self('parent')
            a = args[1]
            rename = a
            if len(args) >= 3:
                rename = args[2]
            fd = Path(self('parent'), a).resolve()
            #print ("_REGISTER_", fd, 'as', rename)
            self('physical')[rename] = fd
            return True
        if args[0] == 'parent':
            return object.__getattribute__(self, 'parent')
        if args[0] == 'items':
            return self(self('state')).items()
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
                    state=args[1], **{old: self(old), 'parent': self('parent')})
        raise Exception('unknow call: ' + str(args) + "\nalso\t" + str(kwargs))

    def __iter__(self):
        return iter(self(self('state')))

    def __remap__(self, d, fromstate='abstract'):
        for key, value in d.items():
            if fromstate == 'physical':
                value = value.read_text()
            if isinstance(value, AbstractNamespace):
                subname = object.__getattribute__(value, 'name')
                print ('!!', key, value, subname)
                value('state', self('state'))
                print ('-->', key, value, subname)
            setattr(self, key, value)

    def __init__(self, name, parent=None, state='abstract', abstract=False, physical=False, ari=False):
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'parent', parent)
        object.__setattr__(self, 'state', state)
        if self('state') == 'abstract':
            object.__setattr__(self, 'datas', dict() if not abstract else abstract)
        elif self('state') == 'physical':
            object.__setattr__(self, 'fs', dict() if not physical else physical)
        if not (abstract is False):
            self.__remap__(abstract, 'abstract')
        if not (physical is False):
            self.__remap__(physical, 'physical')

    def __getattribute__(self, key):
        if key.startswith('__'):
            return object.__getattribute__(self, key)
        else:
            if self('state') == 'abstract':
                return object.__getattribute__(self, 'datas')[key]
            if self('state') == 'physical':
                try:
                    return Path(self('physical')[key]).read_text()
                except Exception as e:
                    raise Exception(f'Error: {Path(self("physical")[key])}')

    def __setattr__(self, key, value):
        if key.startswith('__'):
            raise Exception('Can\'t alter ' + key)
        else:
            if self('state') == 'abstract':
                object.__getattribute__(self, 'datas')[key] = value
            if self('state') == 'physical':
                fs = self('physical')
                #print ('!!', self('parent'))
                fs[key] = self('parent') / Path(key)
                if fs[key].exists():
                    os.remove(str(fs[key]))
                with fs[key].open('w') as f:
                    f.write(value)

    def __str__(self):
        name = {object.__getattribute__(self, 'name')}
        if self('state') == 'abstract':
            return f"[{name}({self('state')}): {str(list(object.__getattribute__(self, 'datas').keys()))}]"
        elif self('state') == 'physical':
            return f"[{name}({self('state')}): {str(list(object.__getattribute__(self, 'fs').keys()))}]"

    def __repr__(self):
        name = {object.__getattribute__(self, 'name')}
        if self('state') == 'abstract':
            return f"[{name}({self('state')}): {str(list(object.__getattribute__(self, 'datas').keys()))}]"
        elif self('state') == 'physical':
            return f"[{name}({self('state')}): {str(list(object.__getattribute__(self, 'fs').keys()))}]"