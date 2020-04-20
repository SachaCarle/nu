import traceback

def card_(tx, style=None): return f"""
<div class="card" {"" if style == None else
"style='" + ';'.join([k + ": " + v for k, v in style.items()]) + ";'"
}>
  <div class="card-body">
  {tx}
  </div>
</div>
"""

def html_(s): return f"""<!DOCTYPE html>
<html>
<body>
{s}
</body>
</html>"""

def code_(s): return f"<code>{s}</code>"

class Handler:
    def find_entity(self, classname, entity_id, *more):
        cls = self.synaps.by_class_entities[classname]
        eid = int(entity_id)
        e = [_ for _ in cls if id(_) == eid]
        assert len(e) != 0, "Entity not found: " + f"{classname}#{eid}"
        return e[0]
    def GET(self, path, *args):
        body = None
        chunks = path.split('/')
        if len(chunks) == 1:
            if chunks[0] in self.synaps.by_class_entities:
                pass # Class specific listing
            else:
                pass # Original or Unknow page
        elif len(chunks) == 2:
            if chunks[0] in self.synaps.by_class_entities:
                try: # Direct class item page
                    et = self.find_entity(*chunks)
                    body = card_(et.html(path))
                except Exception as e:
                    body = card_(code_(traceback.format_exc().replace('\n', '<br>')))
            else:
                pass # Unknow call
        try:
            return self.synaps.html(path, *args, body=body)
        except Exception as e:
            return html_(traceback.format_exc().replace('\n', '<br>'))
