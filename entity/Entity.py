from common import NuObject, AbstractNamespace
import json, os
from pathlib import Path

class Entity(NuObject):
    body = AbstractNamespace('body')
    body.head = AbstractNamespace('head')

    def __init__(self, name=None, def_attrs={}):
        if name != None:
            def_attrs['name'] = name
        else:
            name = def_attrs['name']
        NuObject.__init__(self, **def_attrs)
        self._location = os.path.join(name, 'entity.json')
        with open(self._location, 'w') as f:
            json.dump(self.store, f)

    def awake(self):
        print ('awakening, ', self.head)
        old = os.getcwd()
        os.chdir(os.path.split(self._location)[0])
        mindfile = Path(self.head)
        if not mindfile.exists():
            print ('creating mind')
            with mindfile.open('w') as f:
                f.write("""me.think('hello world!!')""")
        with mindfile.open('r') as f:
            code = mindfile.read_text()
        exec(code, {'me': self})
        os.chdir(old)

    def think(self, *args):
        print (self.name + ':', *args)


#
    def save(self):
        self.think('exit')
        print (dict(self))