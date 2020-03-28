from nujs import ExecuteJs, scripts
from pathlib import Path
import sys, os, subprocess, json, nu, nujs

def cmd(_, args, legacy=True, **kwargs):
    assert args.i
    assert args.o
    code = Path(os.path.join(Path('.').resolve(), Path(args.i))).read_bytes()
    output = Path(os.path.join(Path('.').resolve(), Path(args.o + '.nu')));
    print ("Creating analysing entity at " + str(output))
    tokenizer = scripts['js_tokenizer']
    js = ExecuteJs(fd=tokenizer, stdin=code)
    subprocess.run(["python", "-m", "nu", "create", "-o", args.o])
    codedatafile = Path(output, '.entity', 'entity.json').resolve()
    entity = nu.entity.spirit(codedatafile)
    nu.components.copy('token-visual', entity)
    nu.components.copy('nu-call', entity)
    with Path(entity.location, 'js_tokenizer.js').open('w') as fd:
        fd.write(Path(nujs.scripts['js_tokenizer']).read_text())
    @entity.memory.alter
    def __code__(data):
        data['components']['data'].extend([
            'token-visual', 'nu-call'
            ])
        data['default_body'] = 'body_analyze.html'
        data['analyze'] = {
            'tokens': js.result
        }
        return data
