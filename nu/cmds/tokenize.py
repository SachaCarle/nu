from nujs import ExecuteJs, scripts
from pathlib import Path
import sys, os, subprocess, json, nu

def cmd(_, args, legacy=True, **kwargs):
    assert args.i
    assert args.o
    print ("Creating analysing entity at " + args.o + '.nu')
    tokenizer = scripts['js_tokenizer']
    code = Path(os.path.join(Path('.').resolve(), Path(args.i))).read_bytes()
    output = Path(os.path.join(Path('.').resolve(), Path(args.o + '.nu')));
    js = ExecuteJs(fd=tokenizer, stdin=code)
    #print (js.result)
    subprocess.run(["python", "-m", "nu", "create", "-o", args.o])
    codedatafile = Path(os.path.join(output, '.entity', 'entity.json')).resolve()
    entity = nu.entity.spirit(codedatafile)
    nu.components.copy('token-visual', entity)
    @entity.memory.alter
    def __code__(data):
        data['default_body'] = 'body_analyze.html'
        data['analyze'] = {
            'tokens': js.result
        }
        return data
