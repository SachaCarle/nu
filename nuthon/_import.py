from pathlib import Path
from .template import template
from .execute import execute

def create_code_caller(tr, path):
    code = compile(tr, str(path), 'exec')
    def __code_caller__(locs={}):
        try:
            return exec (code, locs)
        except Exception as e:
            print ('Error trying to execute code: ', tr)
            raise e
    return __code_caller__

def imp(path, env, **more):
    path = Path(path).resolve()
    #print ("NUTHON IMPORT", path)
    #print ('\twith ', env, more)
    tx = path.read_text()
    tn = template(tx)
    #print ('TEMPLATE: ', tn.replace('\n', '\\n'))
    tr = execute(tn, env)
    return create_code_caller(tr, path)