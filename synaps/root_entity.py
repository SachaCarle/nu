from .entity_class import Entity
from sys import stdout
import web

def create_root_entity(synaps):
    class RootEntity(Entity):
        def __init__(self, *s, **kws):
            Entity.__init__(self, *s, **kws)
            self.name = "root"

        def start(root):

            @root
            def think(self, *args):
                stdout.write (self.name + ':' + ', '.join([str(_) for _ in args]) + '\n')
                stdout.flush()


            @root
            def html(self, path, *args, **kw): return f"""<!DOCTYPE html>
<html>
<body>

<h1>{path}</h1>

<p>
{web.ctx}
</p>

</body>
</html>"""
    return RootEntity(synaps)