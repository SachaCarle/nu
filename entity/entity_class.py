from common import NuObject, AbstractNamespace, touchdir, remkdir, json_safe_dict, fun_iterable
import json, os
from pathlib import Path

class Entity(NuObject):

    def integrate(self, fun):
        self(**{fun.__name__: fun})
        return fun

    def __init__(self, name=None, parent=None, def_attrs={}):
        if name != None:
            def_attrs['name'] = name
        else:
            name = def_attrs['name']
        if parent != None:
            def_attrs['parent'] = parent
        elif 'parent' in def_attrs.keys():
            parent = def_attrs['parent']
        NuObject.__init__(self, **def_attrs)
        if name:
            self.name = name
        if parent:
            self.parent = parent

        if parent is None:
            mind_location = Path(os.getcwd(), name, '.entity')
            body_location = Path(os.getcwd(), name)
        elif isinstance(parent, Entity):
            mind_location = Path(os.getcwd(), parent.name, name, '.entity')
            body_location = Path(os.getcwd(), parent.name, name)

        @self.integrate
        def save(fun=None):
            touchdir(body_location)
            touchdir(mind_location)
            if not (fun is None):
                return fun(body_location=body_location, mind_location=mind_location)
            with open(mind_location / 'entity.json', 'w+') as f:
                safe = json_safe_dict(self.store)
                if 'parent' in safe:
                    del safe['parent']
                print (safe)
                json.dump(safe, f)

        @self.integrate
        @fun_iterable
        def items():
            return self.body(self.body('state')).items()

        self.body = AbstractNamespace('body', parent=body_location, state="physical" if not 'body_state' in def_attrs else def_attrs['body_state'])
        self.mind = AbstractNamespace('mind', parent=mind_location, state="abstract" if not 'mind_state' in def_attrs else def_attrs['mind_state'])
        #self.ext = AbstractNamespace('ext')

        @self.integrate
        def create(sub_name, **def_param):
            dp = {
                'state': 'abstract',
                'head': f"me.think('I have been summoned by {name}')",
                **def_param
            }
            return Entity(name=sub_name, parent=self, def_attrs=dp)



    def awake(self):
        old = os.getcwd()
        body = Path(old, self.name)
        os.chdir(str(body))
        if self.state == "physical":
            mind = Path(body, '.entity')
            mindfile = mind / self.head
            if mindfile.exists():
                pass
            else:
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