from .entity_class import Entity
from pprint import pprint


def _print(e, *args, **kwargs):
    if not isinstance(e, Entity):
        return pprint(e, *args, **kwargs)
    print (f"""__{e.name}__
    {e.mind}
    {e.body}
""")