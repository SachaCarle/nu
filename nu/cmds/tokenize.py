from nujs import ExecuteJs, scripts
from pathlib import Path
import sys, os, subprocess, json, nu

def jsonoperate(loc):
    def _jsonoperate(fun):
        d = {}
        if loc.exists():
            with loc.open('r') as fd:
                d = json.load(fd)
            os.remove(loc)
        d = fun(d)
        with loc.open('w') as fd:
            json.dump(d, fd)
    return _jsonoperate

def codereplace(loc, code):
    bodypath = Path(os.path.join(loc, 'body.html')).resolve()
    if bodypath.exists():
        os.remove(bodypath)
    with bodypath.open('w') as fd:
        fd.write(code)

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
    codedatafile = Path(os.path.join(output, 'entity.json')).resolve()
    print (codedatafile)
    @jsonoperate(codedatafile)
    def __code__(data):
        data['default_body'] = 'body_analyze.html'
        data['analyze'] = {
            'tokens': js.result
        }
        return data
