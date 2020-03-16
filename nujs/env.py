import sys, os, subprocess, nu
from pathlib import Path

class ExecuteJs:
    def __init__(self, code=None, fd=None):
        assert code != None or fd != None
        assert code == None or fd == None
        self.state = None

        e_code = """console.log('hello there', __dirname)
        require('./execute_nujs')
        """

        #sub = nu.nupath
        sub = Path('.').resolve()

        ecma5 = Path(os.path.join(sub, '__execute__.js'))
        if not ecma5.exists():
            with ecma5.open('w') as js:
                js.write(e_code)


        exe = Path(os.path.join(sub, 'execute_nujs.js'))

        if exe.exists():
                os.remove(exe)
        if fd:
            with exe.open('w') as js:
                js.write(Path(fd).resolve().read_text())
        elif code:
            if exe.exists():
                os.remove(exe)
            with exe.open('w') as js:
                js.write(code)
        else:
            raise Exception('No param for ExecuteJs')


        print ("!!\t\t", str(ecma5.resolve()), exe)
        self.state = subprocess.run(["node", str(ecma5.resolve())])
        print (self.state)

        #os.remove(exe)
        os.remove(ecma5)