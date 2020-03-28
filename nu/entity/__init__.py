import json, os
from pathlib import Path
# --
from . import constructor

def spirit(entityfile):
    ef = Path(os.getcwd(), entityfile)
    os.chdir(os.path.split(os.path.split(ef)[0])[0])
    if ef.exists():
        jsontxt = ef.read_text()
        entity = json.loads(jsontxt)
        try:
            return constructor.infuse(entity)
        except Exception as er:
            print ('During the construction of ', ef, " an Exception occur:", str(er))
            print ('The entity.json resulted in: ', entity)
            print ('The entity.json was: ', jsontxt)
            raise er
    raise Exception(ef, ": does not exists...")
