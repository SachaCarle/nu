from common import NuObject, AbstractNamespace, touchdir, remkdir, json_safe_dict
import json, os
from pathlib import Path

class Entity(NuObject):

    def __init__(self, name=None, def_attrs={}):
        if name != None:
            def_attrs['name'] = name
        else:
            name = def_attrs['name']
        NuObject.__init__(self, **def_attrs)
        mind_location = Path(os.getcwd(), name, '.entity')
        body_location = Path(os.getcwd(), name)
        def save(fun=None):
            touchdir(body_location)
            touchdir(mind_location)
            with open(mind_location / 'entity.json', 'w+') as f:
                json.dump(json_safe_dict(self.store), f)
            if not (fun is None):
                return fun(body_location=body_location, mind_location=mind_location)
        self(save=save)
        self.body = AbstractNamespace('body', parent=body_location, state="abstract")
        self.mind = AbstractNamespace('mind', parent=mind_location, state="physical")
        #self.ext = AbstractNamespace('ext')



    def awake(self):
        old = os.getcwd()
        print ('awakening:', old, self.name, self.head)
        body = Path(old, self.name)
        os.chdir(str(body))
        if self.state == "physical":
            mind = Path(body, '.entity')
            mindfile = mind / self.head
            if mindfile.exists():
                pass
            else:
                print ('creating mind', mindfile.exists(), mindfile)
                with mindfile.open('w') as f:
                    f.write("""me.think('hello world!!')""")
            with mindfile.open('r') as f:
                code = mindfile.read_text()
        else:
            code = self.head
        exec(code, {'me': self})
        os.chdir(old)

    def think(self, *args):
        print (self.name + ':', *args)