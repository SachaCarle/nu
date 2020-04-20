from .entity_class import Entity
from sys import stdout
import traceback
import web

def create_root_entity(synaps):
    class RootEntity(Entity):
        def __init__(self, *s, **kws):
            Entity.__init__(self, *s, **kws)
            self.name = "root"

        def start(root):
            @root

            @root
            def urlbar(self, path):
                return card_(f"""<h1><a href='/'>HOME</a> / <a>{path}</a></h1>
""")

            @root
            def entity_list(self, el, name="UNDEFINED"):
                s = "<div>"
                for e in el:
                    try:
                        if e is self:
                            s += card_("<p>Root</p>")
                        else:
                            s += card_(e('html'))
                    except Exception as er:
                        _s = f"<p>{e.name}Exception: {repr(er)}<p><br>" + name + "<br>" + traceback.format_exc().replace('\n', '<br>')
                        s += card_(_s)
                    s += "<br>"
                s += "</div>"
                return s
            @root
            def html(self, path, *args, **kw): return f"""<!DOCTYPE html>
<html>
{synaps.head(path, *args, **kw)}
<body>
{self('urlbar', path)}
{"<br>".join(["<h3>" + K + "<h3><br>" + root('entity_list', L, K)
    for K,L in synaps.by_name_entities.items()]) }
</body>
</html>"""
    return RootEntity(synaps)